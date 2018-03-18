# Design the Twitter timeline and search

related questions:

- **Design the Facebook feed**

- **Design Facebook search**

## Step 1: Outline use cases and constraints

### Use cases

* **User** posts a tweet
    * **Service** pushes tweets to followers, sending push notifications and emails
* **User** views the user timeline (activity from the user)
* **User** views the home timeline (activity from people the user is following)
* **User** searches keywords
* **Service** has high availability

### Constraints

**General**

* Traffic is not evenly distributed
* Posting a tweet should be fast
    * Fanning out a tweet to all of your followers should be fast, unless you have millions of followers
* 100 million active users
* 500 million tweets per day or 15 billion tweets per month
    * Each tweet averages a fanout of 10 deliveries
    * 5 billion total tweets delivered on fanout per day
    * 150 billion tweets delivered on fanout per month
* 250 billion read requests per month
* 10 billion searches per month

**Timeline**

* Viewing the timeline should be fast
* Twitter is more read heavy than write heavy
    * Optimize for fast reads of tweets
* Ingesting tweets is write heavy

**Search**

* Searching should be fast
* Search is read-heavy

### Load parameters


* 150 TB of new tweet content per month
    * 10 KB per tweet * 500 million tweets per day * 30 days per month
    * 5.4 PB of new tweet content in 3 years
    * Size per tweet:
        * `tweet_id` - 8 bytes
        * `user_id` - 32 bytes
        * `text` - 140 bytes
        * `media` - 10 KB average
        * Total: ~10 KB
* 100k read requests per second
    * 250 billion read requests per month / (2.5 Million seconds per month)
* 6k tweets/writes per second
    * 15 billion tweets per month / (2.5 Million seconds per month)
* 60k  tweets delivered on fanout per second
    * 150 billion tweets delivered on fanout per month / (2.5 Million seconds per month)
* 4k search requests per second
* [handy conversion](back-of-env/#handy-conversion-guide)

## Step 2: Create a high level design

> Outline a high level design with all important components.

![Imgur](http://i.imgur.com/48tEA2j.png)

## Step 3: Design core components

> Dive into details for each core component.

### Use case: User posts a tweet

#### Pick different data store for different services

We could store the user's own tweets to populate the user timeline (activity from the user) in a [relational database](https://github.com/donnemartin/system-design-primer#relational-database-management-system-rdbms).

Delivering tweets and building the home timeline (activity from people the user is following) is trickier.  Fanning out tweets to all followers (60 thousand tweets delivered on fanout per second) will overload a traditional [relational database](https://github.com/donnemartin/system-design-primer#relational-database-management-system-rdbms).  We'll probably want to choose a data store with fast writes such as a **NoSQL database** or **Memory Cache**.  Reading 1 MB sequentially from memory takes about 250 microseconds, while reading from SSD takes 4x and from disk takes 80x longer.<sup><a href=https://github.com/donnemartin/system-design-primer#latency-numbers-every-programmer-should-know>1</a></sup>

We could store media such as photos or videos on an **Object Store**.

* The **Client** posts a tweet to the **Web Server**, running as a [reverse proxy](https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server)
* The **Web Server** forwards the request to the **Write API** server
* The **Write API** stores the tweet in the user's timeline on a **SQL database**
* The **Write API** contacts the **Fan Out Service**, which does the following:
    * Queries the **User Graph Service** to find the user's followers stored in the **Memory Cache**
    * Stores the tweet in the *home timeline of the user's followers* in a **Memory Cache**
        * O(n) operation:  1,000 followers = 1,000 lookups and inserts

        * We'll need to access the timeline tweets in chronological order later, from the most recent update to the oldest, so the perfect kind of data structure for this is a List. Basically every new update will be LPUSHed in the user updates key, and thanks to LRANGE, we can implement pagination and so on.

        * Each post is just represented by a Hash with three fields. The ID of the user owning the post, the time at which the post was published, and finally, the body of the post, which is, the actual status message.

        * After we create a post and we obtain the post ID, we need to LPUSH the ID in the timeline of every user that is following the author of the post.

        * [use redis store to implement twitter](https://redis.io/topics/twitter-clone)

    * Stores the tweet in the **Search Index Service** to enable fast searching
    * Stores media in the **Object Store**
    * Uses the **Notification Service** to send out push notifications to followers:
        * Uses a **Queue** (not pictured) to asynchronously send out notifications

If our **Memory Cache** is Redis, we could use a native Redis list with the following structure:

```
           tweet n+2                   tweet n+1                   tweet n
| 8 bytes   8 bytes  1 byte | 8 bytes   8 bytes  1 byte | 8 bytes   8 bytes  1 byte |
| tweet_id  user_id  meta   | tweet_id  user_id  meta   | tweet_id  user_id  meta   |
```

The new tweet would be placed in the **Memory Cache**, which populates user's home timeline (activity from people the user is following).

```
INCR next_post_id => 10343
HMSET post:10343 user_id $owner_id time $time body "I'm having fun with Retwis"
```

We'll use a public [**REST API**](https://github.com/donnemartin/system-design-primer#representational-state-transfer-rest):

```
$ curl -X POST --data '{ "user_id": "123", "auth_token": "ABC123", \
    "status": "hello world!", "media_ids": "ABC987" }' \
    https://twitter.com/api/v1/tweet
```

Response:

```
{
    "created_at": "Wed Sep 05 00:37:15 +0000 2012",
    "status": "hello world!",
    "tweet_id": "987",
    "user_id": "123",
    ...
}
```

For internal communications, we could use [Remote Procedure Calls](https://github.com/donnemartin/system-design-primer#remote-procedure-call-rpc).

### Use case: User views the home timeline

* The **Client** posts a home timeline request to the **Web Server**
* The **Web Server** forwards the request to the **Read API** server
* The **Read API** server contacts the **Timeline Service**, which does the following:
    * Gets the timeline data stored in the **Memory Cache**, containing tweet ids and user ids - O(1)
    * Queries the **Tweet Info Service** with a [multiget](http://redis.io/commands/mget) to obtain additional info about the tweet ids - O(n)
    * Queries the **User Info Service** with a multiget to obtain additional info about the user ids - O(n)

REST API:

```
$ curl https://twitter.com/api/v1/home_timeline?user_id=123
```

Response:

```
{
    "user_id": "456",
    "tweet_id": "123",
    "status": "foo"
},
{
    "user_id": "789",
    "tweet_id": "456",
    "status": "bar"
},
{
    "user_id": "789",
    "tweet_id": "579",
    "status": "baz"
},
```

### Use case: User views the user timeline

* The **Client** posts a user timeline request to the **Web Server**
* The **Web Server** forwards the request to the **Read API** server
* The **Read API** retrieves the user timeline from the **SQL Database**

The REST API would be similar to the home timeline, except all tweets would come from the user as opposed to the people the user is following.

### Use case: User searches keywords

* The **Client** sends a search request to the **Web Server**
* The **Web Server** forwards the request to the **Search API** server
* The **Search API** contacts the **Search Service**, which does the following:
    * Parses/tokenizes the input query, determining what needs to be searched
        * Removes markup
        * Breaks up the text into terms
        * Fixes typos
        * Normalizes capitalization
        * Converts the query to use boolean operations
    * Queries the **Search Cluster** (ie [Lucene](https://lucene.apache.org/)) for the results:
        * [Scatter gathers](https://github.com/donnemartin/system-design-primer#under-development) each server in the cluster to determine if there are any results for the query
        * Merges, ranks, sorts, and returns the results

REST API:

```
$ curl https://twitter.com/api/v1/search?query=hello+world
```

The response would be similar to that of the home timeline, except for tweets matching the given query.

## Step 4: Scale the design

> Identify and address bottlenecks, given the constraints.

![Imgur](http://i.imgur.com/jrUBAF7.png)

The **Fanout Service** is a potential bottleneck.  Twitter users with millions of followers could take several minutes to have their tweets go through the fanout process.  This could lead to race conditions with @replies to the tweet, which we could mitigate by re-ordering the tweets at serve time.

We could also avoid fanning out tweets from highly-followed users.  Instead, we could search to find tweets for high-followed users, merge the search results with the user's home timeline results, then re-order the tweets at serve time.

Additional optimizations include:

* Keep only several hundred tweets for each home timeline in the **Memory Cache**
* Keep only active users' home timeline info in the **Memory Cache**
    * If a user was not previously active in the past 30 days, we could rebuild the timeline from the **SQL Database**
        * Query the **User Graph Service** to determine who the user is following
        * Get the tweets from the **SQL Database** and add them to the **Memory Cache**
* Store only a month of tweets in the **Tweet Info Service**
* Store only active users in the **User Info Service**
* The **Search Cluster** would likely need to keep the tweets in memory to keep latency low

We'll also want to address the bottleneck with the **SQL Database**.

Although the **Memory Cache** should reduce the load on the database, it is unlikely the **SQL Read Replicas** alone would be enough to handle the cache misses.  We'll probably need to employ additional SQL scaling patterns.

The high volume of writes would overwhelm a single **SQL Write Master-Slave**, also pointing to a need for additional scaling techniques.

* [Federation](https://github.com/donnemartin/system-design-primer#federation)
* [Sharding](https://github.com/donnemartin/system-design-primer#sharding)
* [Denormalization](https://github.com/donnemartin/system-design-primer#denormalization)
* [SQL Tuning](https://github.com/donnemartin/system-design-primer#sql-tuning)

We should also consider moving some data to a **NoSQL Database**.
