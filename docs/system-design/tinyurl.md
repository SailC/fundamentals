## Reference

[http://blog.gainlo.co/index.php/2016/03/08/system-design-interview-question-create-tinyurl-system/](http://blog.gainlo.co/index.php/2016/03/08/system-design-interview-question-create-tinyurl-system/)

[https://www.educative.io/collection/page/5668639101419520/5649050225344512/5668600916475904](https://www.educative.io/collection/page/5668639101419520/5649050225344512/5668600916475904)

[Tiny Url](https://www.notion.so/564b8d02-6d0a-4291-abd0-00ec7a7336b9)

[https://soulmachine.gitbooks.io/system-design/content/cn/tinyurl.html](https://soulmachine.gitbooks.io/system-design/content/cn/tinyurl.html)

[https://segmentfault.com/a/1190000006140476](https://segmentfault.com/a/1190000006140476)

[短 URL 系统是怎么设计的？ - 知乎](https://www.zhihu.com/question/29270034)

---

## Problem & Features

## QPS & Storage Estimation

![](https://static.notion-static.com/dce64687-02f9-4033-b753-28dd04ae80c9/Scannable_Document_on_Dec_24_2017_at_4_11_31_PM.png)

- If we are not sure about the load parameters, always start with smaller estimate. The purpose is to come up with a working solution and then talk about how to scale
- Since peak read QPS is only about 2k, a single SQL server can handle the load.
- Since it only takes 1TB storage space in 3 years, a single Machine with more than 1TB hard drive can provide enough storage space.

## Basical Architecture



![](https://static.notion-static.com/a9c1154f-4e92-4606-910c-2aee1f61168f/Scannable_Document_on_Dec_24_2017_at_4_50_57_PM.png)

1. Client / Broswer sends a GET request (client can directly hit end point [goo.gl/Xabr0z](http://goo.gl/Xabr0z) or use API goo.gl/v1/url?shortURL=Xabr0z)
1. Client sends a POST request (e.g. client can directly hit end point [goo.gl/v1/url](http://goo.gl/v1/url) or use web page UI to send Ajax call to the end point {longURL: www.example.com})
1. App server listening to the end point calls the event handler according to the request type. If the request is of type GET, then `UrlService.shortToLong` is called. If the request is of type POST, then `UrlService.longToShort`  is called.
1. Both encoding/decoding action needs to talk to the SQL db to query the db index.
1. SQL db is used to make sure that a single short URL is only mapped to only one single long URL.
1. After getting the long url (GET) / creating the short url (POST), the UrlService send the result back to the app server
1. app server sends the response back to the client. If it's a GET request, client gets a 302 redirect http response and gets redirected to the long url. If it's a post request, client will get 200 if the post action is successful.

# API

## REST API

1. GET - Expand a short URL
  - Request `GET [https://www.googleapis.com/urlshortener/v1/url?shortUrl=http://goo.gl/fbsS](https://www.googleapis.com/urlshortener/v1/url?shortUrl=http://goo.gl/fbsS)`
  - Response

      {
       "kind": "urlshortener#url",
       "id": "http://goo.gl/fbsS",
       "longUrl": "http://www.google.com/",
       "status": "OK"
      }

1. POST - Shorten a long URL
  - Request

      POST https://www.googleapis.com/urlshortener/v1/url
      Content-Type: application/json

      {"longUrl": "http://www.google.com/"}

  - Response

      {
       "kind": "urlshortener#url",
       "id": "http://goo.gl/fbsS",
       "longUrl": "http://www.google.com/"
      }

- see [https://developers.google.com/url-shortener/v1/getting_started#actions](https://developers.google.com/url-shortener/v1/getting_started#actions) for more details

## Application Logic

Approach I `Alias Hash`  : Randomly generate short URL and use hashtable / database to prevent the same shortURL mapping to mutiple longURLs.

    class UrlService {
    	constructor() {
            this.l2s = new Map(); // simulate secondary index for long URL
            this.s2l = new Map(); // simulate primary index for short URL
    	}

        longToShort(url) {
            if (this.l2s.has(url)) return this.l2s.get(url);
            while (true) {
                let shortUrl = this.generateShortUrl();
                if (this.s2l.has(shortUrl)) continue;
                this.s2l.set(shortUrl, url);
                this.l2s.set(url, shortUrl);
                return shortUrl;
            }
        }

        shortToLong(url) {
            if (!this.s2l.has(url)) return null;
            return this.s2l.get(url);
        }

        generateShortUrl() {
            let charPool = '0123456789' + 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.toUpperCase();
            let shortUrl = 'http://tiny.url/';
            let suffix = [];
            const SUFFIX_LEN = 6;
            for (let i = 0; i < SUFFIX_LEN; i++) {
                let index = ~~(Math.random() * charPool.length);
                suffix.push(charPool[index]);
            }
            return shortUrl + suffix.join('');
        }
    }

    let tinyUrl = new UrlService();
    let shortURL = tinyUrl.longToShort('www.youtube.com');
    console.log(tinyUrl.shortToLong(shortURL));

Approach II : Use global incremental id to map to a short URL using base62 encoding.  

[Distributed ID generator](https://www.notion.so/004c52f4-f27d-4a78-8fe8-526347ef35a2)

    class UrlService {
    	constructor() {
            this.gid = 0; //global id
            this.id2Url = new Map(); // simulate primary index for id
            this.url2Id = new Map(); // simulate secondary index for Long URL
    	}

        longToShort(url) {
            let id = this.url2Id.get(url) || (this.gid++);
            this.url2Id.set(url, id);
            this.id2Url.set(id, url);
            let suffix = this._idToBase62(id);
            let shortUrl = 'http://tiny.url/' + suffix;
            return shortUrl;
        }

        shortToLong(url) {
            let prefixLen = "http://tiny.url/".length;
            let shortKey = url.slice(prefixLen);
            let id = this._base62ToId(shortKey);
            return this.id2Url.get(id);
        }

        _idToBase62(id) {
            let charPool = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
            let suffix = [];
            while (id > 0) {
                let c = charPool[id % 62];
                suffix.unshift(c);
                id = ~~(id / 62);
            }
            while (suffix.length < 6) suffix.unshift('0');
            return suffix.join('');
        }

        _base62ToId(str) {
            let charPool = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
            let id = 0;
            for (let c of str) {
                id = id * 62 + charPool.indexOf(c);
            }
            return id;
        }

    }

Reasons to pick Hashing approach

- If the system allows the user to set custom short URLs, using `alias hashing`  is easier to implement because we can just calculate the corresponding hash in the same way.

Reasons to pick auto incremental id approach

- hash function has conflict and will impact performance when facing heavy load. Auto incremental id make sure no conflict will happen.
- sequential insertion of the db record is much faster than random insertion

## DB Schema

We would need two tables, one for storing information about the URL mappings and the other for users’ data (if we're asked to do so by the interviewer).

![](https://static.notion-static.com/06b4de2f-7b18-407d-a48b-0c5d8f0bcd04/Screen_Shot_2017-12-24_at_6.24.44_PM.png)

Reasons to pick SQL db:

- global auto incremental id
- QPS requirement is not very high intially (when we don't have a lot DAU and uses requests are not very demanding)

Reasons to pick noSQL db:

- The data of our application is simply just key value pairs, not very highly interconnected.  (we don't need to use SQL join to perform complicated query).
- Once the load of our system becomes heavier, we can scale more easily with NoSQL dbs.

## Scalable Architecture

![](https://static.notion-static.com/ab5faf84-0a42-40fd-ab58-6f27f86b256f/Whiteboard_on_Dec_24_2017_at_9_22_46_PM.jpg)

- How much cache should we have?

We can start with 20% of daily traffic and based on clients’ usage pattern we can adjust how many cache servers we need. As estimated above we need 170GB memory to cache 20% of daily traffic since a modern day server can have 256GB memory, we can easily fit all the cache into one machine, or we can choose to use a couple of smaller servers to store all these hot URLs.

- Which cache eviction policy would best fit our needs?

When the cache is full, and we want to replace a link with a newer/hotter URL, how would we choose? Least Recently Used (LRU) can be a reasonable policy for our system

- How can we partition the database when the we are running out of cache resources?
  1. Key range partition . Easy to create uneven distribution, which leads to bottleneck.
  1. Hash partition
- we can continue using the global incremental id.
  - for GET request, a shortUrl is decoded to a global id , and we can mod that id to the total number of db machines and find the db machine.
  - for POST request, we broadcast the longURL to all the db machines and check if it exist.
  - we can use a single machine to maintain that global incremental id , but this will create bottleneck. Adding standby machines makes the system more complicated.
- Can we get away without using global incremental id?
  - We add a extra partition character in the shortURL to indicate the db machine which has the mapping.
  - for GET request, the parition id is parsed from shortURL and that points to the db machine.
  - for POST request, use consistent hash to map the longURL to one of the db machine, we the incremental id of that machine to generate shortURL and insert the db machine id to the first character of the shortURL.
- How to rebalance the mapping distribution when new machiens comes in ?
  - Find the machine who owns the largest range and split it into half. The new machine takes a half of the range.

# Follow up

## how to support custom urls ?

- create another table which maps `custom url`  to `long url` . For `GET`  request, first check `custom url`  table, then check `short url`  table. For `post`  request, insert to the `custom url`  table and skip the `short url`  table.
- Why not add a new column in `short url`  table ? because for most rows that field would be empty. we don't want to create a sparse db table which takes extra space.

## Can we allow one Long url map to mutiple short urls ?

Reasons for one to many mapping:

1. mutiple short urls can contain different analytics data (e.g. use location, broswer agent, countries, os...) all kinds of click stats

Reasons for one to one mapping:

1. save extra space to store the mapping.
1. some malacious users would send huge volume of `POST`  requests of the same longURL to exhaust the incremental ids.

If we are implementing a simple service , than one to one mapping can save us space. But if we need to explore the user behavior and analyze the data, using one to many mapping can give us more room to store the analytic data.

## 301 or 302?

If `GET`  request returns a  `301 permanent redirection` , The client/browser would not attempt to request the original location but use the new location from now on. Most modern browsers cache 301s and won't bother requesting the original source at all for up to 6 months,  Which is bad for us because that prevents the future user requests to hit our UrlService endpoint and we have no way to collect the click stats if that happens.

`Status 302`  means that the resource is temporarily located somewhere else, and the client/browser should continue requesting the original url. So if the user click the short url in the future, it's still gonna hit our back end service and we can keep track of the users click stats.

[HTTP redirect: 301 (permanent) vs. 302 (temporary)](https://stackoverflow.com/a/18556097)

## How to prevent hackers exausting ids.

- Use Rate limiter to limit the number of request for a user during a time span.
- Create LRU cache for `longURL→ shortURL` mapping , only store the data in one day.  if the hacker sends lots of `POST`  request with the same `longURL`  in one day, we just return the cached result.

# Topic covered:

1. Distributed ID generator
1. Consistent Hashing
1. Rate Limiter
1. Database sharding

---

David

[https://www.interviewcake.com/question/java/url-shortener](https://www.interviewcake.com/question/java/url-shortener)

There are 2 ways to go about this:

1. Brainstorm issues then revise

  2.  Brainstorm design goals, then design around the design goals

# W**hat are we building? (Problem)**

We are building a site that shortens a url given a normal url string. The shortened url will typically have something along the lines of [bit.ly/a12bc](http://bit.ly/a12bc)

# **What features might we need? (Features)**

We will need an api to encode and decode the url to start.

*We should question the interviewer for details as we start going along with our thinking*

**Q for Interviewer:**

- Is this api going to be open or closed (Require developer secrets/keys)?
  - If yes, we will need to add a developer key parameter in our api
- Can people delete the links? Do they persist forever?
  - If yes, add an api to delete the links
  - If no, we must have some policies in place for links:
    1. Remove links we created a certain time length ago (Time)
    1. Remove links that are not visited (Frequency)
  - Auto generated link? Choose your own?
  - Analytics?

# Design Goals (Constraints)

Come up with a system that:

- Stores lots of links
- Redirecting a shortlink should be fast
- Resilient to load spikes

# Data Model

    // Link:
    //	- shortLink: slug
    //	- longLink:  destination

    // Psuedocode for API:

    // Link for get slug
    // we want linkto be something like: [bit.ly/v1/shortLink](http://bit.ly/v1/shortLink)

    // Example:
    $ curl --data '{"destination": "mywebpagetoshorten.com"}' https://bit.ly/api/v1/shortlink
    {
      "slug": "ae8uFt",
      "destination": "mywebpagetoshorten.com"
    }

    // Endpoint
    public Response shortlink(Request request) {
        if (request.method() != HttpMethod.POST) {
            return new Response(HttpStatus.ERROR501);  // 501 NOT IMPLEMENTED
        }

        String destination = request.getData().getDestination();
        String slug = request.getData().getSlug();

        // if the request did not include a slug, make a new one
        if (slug == null) {
            slug = generateRandomSlug();
        }

        DB.insertLink(slug, destination);

        String responseBody = String.format("{'slug':'%s'}", slug);

        return new Response(HttpStatus.OK200, responseBody);
    }

    // On client end:
    // Redirect the response
    function redirect(request) {
        var destination = DB.getLinkDestination(request.path);
        return response(302, destination);
    }

# Implementing Unique Links

We can have n^c combinations of links where c is the length of the link and n is the variations for each character. Given that these characters need to be in urls, we should only use alphanumeric characters [a-zA-Z0-9] = 26 + 26 + 10 = 62

How many short urls do we need to accomodate? - ask interviewer, or  - estimate:

Assume upperbound of QPS: 20 links per second * 60 * 60 * 24 * 365= 640M, stores for 5 years = 3T

Look online for what 62^c = 3T ——>  6.9 = 7. Thus our length can be around 7

We can generate new links through a random generator that pulls from aphanumeric characters. What happens when we hit a conflict though?

1. We can re-roll
1. Better yet, increase by 1 and convert to base 62

# Web server architecture

Have a standard db with caching for more popular websites.
