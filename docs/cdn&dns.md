# CDN & DNS

## 你 type google.com 的时候都发生了什么
![1](https://static.notion-static.com/608f10253a944c73979b94e091eb8f35/v2-24ad4aca2ad7b189c70a8b5d29e00850_r.jpg)

1. you enter a url in the browser
2. the browser looks up the ip address for the domain name
  - broswer cache (caches contents for 2 ~ 30mins)
  - OS cache (makes a system call to gethostname)
  - router cache
  - ISP DNS cache
  - Recursive search
    - root name server -> .com name server -> .google name server
3. the broswer sends the http request to the server
  - GET request
    - URL
    - User Agent
    - Cookie (track the state of a website between requests)
    - Accept ?
    - Connection (keep the state of a website between requests)
  - POST request
    - sends parameters in the request body while GET sends its parameters in URL
4. the google server responds with a permanant redirect
  - server sends back 301 (moved permanantly) is for search engine rankings (two urls means fewer incoming links & lower rankings each). Search engine understand permant redict and will combine the incomming links into a single ranking
  - also, multiple urls for the same content are not cache friendly.
5. the broswer follows the redict and hit the end server
6. the server handles the request
  - hit reverse proxy first
  - hit the request handler , which reads the request, parameters & cookies and generate html response
7. the server sends back a HTML response
  - `content-encoding` tells the brower that the response body is compressed using gzip.
  - `cache-control` specify whether and how to cache the page
  - `content-type` is set to `text/html`, which tells the brower to interpret it as html, not download it as a file.
8. the browser begins rendering the HTML
9. the browser sends requests for resources embeded in HTML
  - HTML contains external links, each will go through a similar process to what the HTML page go through
  - static files allow the browswer to cache them. The response of the returned file contains the `Expires` header. `ETag` header is like a version number, if the browswer sees a version number it already has, it will stop the transfer immediately.
10. the broswer sends further asynchronouse (AJAX) requests
  - facebook updating your login friends
  - pull the server for updated info
  - long pulling

## Domain name system

<p align="center">
  <img src="http://i.imgur.com/IOyLj4i.jpg">
  <br/>
  <i><a href=http://www.slideshare.net/srikrupa5/dns-security-presentation-issa>Source: DNS security presentation</a></i>
</p>

A Domain Name System (DNS) translates a domain name such as www.example.com to an IP address.

DNS is hierarchical, with a few authoritative servers at the top level.  Your router or ISP provides information about which DNS server(s) to contact when doing a lookup. DNS results can also be cached by your browser or OS for a certain period of time, determined by the [time to live (TTL)](https://en.wikipedia.org/wiki/Time_to_live).

* **NS record (name server)** - Specifies the DNS servers for your domain/subdomain. `ns1.vultr.com` `ns2.vultr.com`

* **MX record (mail exchange)** - Specifies the mail servers for accepting messages. `hefumiyabi.com`
* **A record (address)** - Points a name to an IP address. `104.238.150.164
`
* **CNAME (canonical)** - Points a name to another name or `CNAME` (example.com to www.example.com) or to an `A` record. `hefumiyabi.com`

### Disadvantage(s): DNS

* Accessing a DNS server introduces a slight delay, although mitigated by caching described above.
* DNS server management could be complex and is generally managed by [governments, ISPs, and large companies](http://superuser.com/questions/472695/who-controls-the-dns-servers/472729).
* DNS services have recently come under [DDoS attack](http://dyn.com/blog/dyn-analysis-summary-of-friday-october-21-attack/), preventing users from accessing websites such as Twitter without knowing Twitter's IP address(es).

## Content delivery network

<p align="center">
  <img src="http://i.imgur.com/h9TAuGI.jpg">
  <br/>
  <i><a href=https://www.creative-artworks.eu/why-use-a-content-delivery-network-cdn/>Source: Why use a CDN</a></i>
</p>

A content delivery network (CDN) is a globally distributed network of proxy servers, serving content from locations closer to the user.  Generally, static files such as HTML/CSS/JS, photos, and videos are served from CDN, although some CDNs such as Amazon's CloudFront support dynamic content.  The site's DNS resolution will tell clients which server to contact.

Serving content from CDNs can significantly improve performance in two ways:

* Users receive content at data centers close to them
* Your servers do not have to serve requests that the CDN fulfills

### Push CDNs

Push CDNs receive new content whenever changes occur on your server.  You take full responsibility for providing content, uploading directly to the CDN and rewriting URLs to point to the CDN.  You can configure when content expires and when it is updated.  Content is uploaded only when it is new or changed, minimizing traffic, but maximizing storage.

Sites with a small amount of traffic or sites with content that isn't often updated work well with push CDNs.  Content is placed on the CDNs once, instead of being re-pulled at regular intervals.

### Pull CDNs

Pull CDNs grab new content from your server when the first user requests the content.  You leave the content on your server and rewrite URLs to point to the CDN.  This results in a slower request until the content is cached on the CDN.

A [time-to-live (TTL)](https://en.wikipedia.org/wiki/Time_to_live) determines how long content is cached.  Pull CDNs minimize storage space on the CDN, but can create redundant traffic if files expire and are pulled before they have actually changed.

Sites with heavy traffic work well with pull CDNs, as traffic is spread out more evenly with only recently-requested content remaining on the CDN.

### Disadvantage(s): CDN

* CDN costs could be significant depending on traffic, although this should be weighed with additional costs you would incur not using a CDN.
* Content might be stale if it is updated before the TTL expires it.
* CDNs require changing URLs for static content to point to the CDN.
