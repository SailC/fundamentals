# Design a web crawler

- [jiuzhang solution](https://www.jiuzhang.com/solution/webpage-crawler/#tag-highlight-lang-python)

## Step 1: Outline use cases and constraints

### Use cases

* **Service** crawls a list of urls:
    * Generates reverse index of words to pages containing the search terms
    * Generates titles and snippets for pages
        * Title and snippets are static, they do not change based on search query
* **User** inputs a search term and sees a list of relevant pages with titles and snippets  the crawler generated
    * Only sketch high level components and interactions for this use case, no need to go into depth
* **Service** has high availability

#### Out of scope

* Search analytics
* Personalized search results
* Page rank

#### Constraints

* Traffic is not evenly distributed
    * Some searches are very popular, while others are only executed once
* Support only anonymous users
* Generating search results should be fast
* The web crawler should not get stuck in an infinite loop
    * We get stuck in an infinite loop if the graph contains a cycle
* 1 billion links to crawl 写
    * Pages need to be crawled regularly to ensure freshness
    * Average refresh rate of about once per week, more frequent for popular sites
        * 4 billion links crawled each month
    * Average stored size per web page: 500 KB
        * For simplicity, count changes the same as new pages
* 100 billion searches per month 读

Exercise the use of more traditional systems - don't use existing systems such as [solr](http://lucene.apache.org/solr/) or [nutch](http://nutch.apache.org/).

#### Load parameters

* 2 PB of stored page content per month
    * 500 KB per page * 4 billion links crawled per month
    * 72 PB of stored page content in 3 years
* 1,600 write requests per second
* 40,000 search requests per second

Handy conversion guide:

* 2.5 million seconds per month
* 1 request per second = 2.5 million requests per month
* 40 requests per second = 100 million requests per month
* 400 requests per second = 1 billion requests per month

## Step 2: Create a high level design

> Outline a high level design with all important components.

![Imgur](http://i.imgur.com/xjdAAUv.png)

## Step 3: Design core components

> Dive into details for each core component.

### Use case: Service crawls a list of urls

We'll assume we have an initial list of `links_to_crawl` ranked initially based on overall site popularity.  If this is not a reasonable assumption, we can seed the crawler with popular sites that link to outside content such as [Yahoo](https://www.yahoo.com/), [DMOZ](http://www.dmoz.org/), etc

#### Prototype
Initially, when working on the prototype, we can use an in memory `URL queue` to store the `links_to_crawl`, given some popular seed and use bread first seach to crawl the webpages.

Breadth first or depth first? Breadth-first search (BFS) is usually used. However, Depth First Search (DFS) is also utilized in some situations, such as if your crawler has already established a connection with the website, it might just DFS all the URLs within this website to save some handshaking overhead.

We can start from single thread crawling, later switch to multiple threads crawling from the `links_to_crawl` queue because single thread would spend too much time waiting for IO operations.

When we switch to multi-threading model, we have to be careful about the concurrency issue when producing & consume urls from the same in memory queue. e.g.

* N consumers (page loader) load N url page at the same time while in fact there's only M urls in the queue (M < N).
* N producers (url extractor) put N urls into the queue while actually only M empty slots are left (M < N).
* Since the read / write operation are not atomic, race condition happens frequently when large # of threads are created.

Due to the concurrency & memory size limit, we consider to use message broker like redis(which provide persistent storage) to hold the `links_to_crawl`.

#### Work flow  

We'll use a table `crawled_links` to store processed links and their page signatures.

We could store `links_to_crawl` and `crawled_links` in a key-value **NoSQL Database**.  For the ranked links in `links_to_crawl`, we could use [Redis](https://redis.io/) with sorted sets to maintain a ranking of page links.  We should discuss the [use cases and tradeoffs between choosing SQL or NoSQL](https://github.com/donnemartin/system-design-primer#sql-or-nosql).

* The **Crawler Service** processes each page link by doing the following in a loop:
    * Takes the top ranked page link to crawl from `links_to_crawl`. 采用优先队列调度，区别于单纯的BFS，对于每个网页设定一定的抓取权重，优先抓取权重较高的网页。
        1. 是否属于一个比较热门的网站
        2. 链接长度
        3. link到该网页的网页的权重
        4. 该网页被指向的次数 等等
    * Checks `crawled_links` in the **NoSQL Database** for an entry with a similar page signature
    * If we have a similar page, reduces the priority of the page link
        * This prevents us from getting into a cycle
        * Continue
    * Else, crawls the link
        * Adds a job to the **Reverse Index Service** queue to generate a [reverse index](https://en.wikipedia.org/wiki/Search_engine_indexing)
        * Adds a job to the **Document Service** queue to generate a static title and snippet
        * Generates the page signature
        * Removes the link from `links_to_crawl` in the **NoSQL Database**
        * Inserts the page link and signature to `crawled_links` in the **NoSQL Database**

**Clarify with your interviewer how much code you are expected to write**.

`PagesDataStore` is an abstraction within the **Crawler Service** that uses the **NoSQL Database**:

```
class PagesDataStore(object):

    def __init__(self, db);
        self.db = db
        ...

    def add_link_to_crawl(self, url):
        """Add the given link to `links_to_crawl`."""
        ...

    def remove_link_to_crawl(self, url):
        """Remove the given link from `links_to_crawl`."""
        ...

    def reduce_priority_link_to_crawl(self, url)
        """Reduce the priority of a link in `links_to_crawl` to avoid cycles."""
        ...

    def extract_max_priority_page(self):
        """Return the highest priority link in `links_to_crawl`."""
        ...

    def insert_crawled_link(self, url, signature):
        """Add the given link to `crawled_links`."""
        ...

    def crawled_similar(self, signature):
        """Determine if we've already crawled a page matching the given signature"""
        ...
```

`Page` is an abstraction within the **Crawler Service** that encapsulates a page, its contents, child urls, and signature:

```
class Page(object):

    def __init__(self, url, contents, child_urls, signature):
        self.url = url
        self.contents = contents
        self.child_urls = child_urls
        self.signature = signature
```

`Crawler` is the main class within **Crawler Service**, composed of `Page` and `PagesDataStore`.

```
class Crawler(object):

    def __init__(self, data_store, reverse_index_queue, doc_index_queue):
        self.data_store = data_store
        self.reverse_index_queue = reverse_index_queue
        self.doc_index_queue = doc_index_queue

    def create_signature(self, page):
        """Create signature based on url and contents."""
        ...

    def crawl_page(self, page):
        for url in page.child_urls:
            self.data_store.add_link_to_crawl(url)
        page.signature = self.create_signature(page)
        self.data_store.remove_link_to_crawl(page.url)
        self.data_store.insert_crawled_link(page.url, page.signature)

    def crawl(self):
        while True:
            page = self.data_store.extract_max_priority_page()
            if page is None:
                break
            if self.data_store.crawled_similar(page.signature):
                self.data_store.reduce_priority_link_to_crawl(page.url)
            else:
                self.crawl_page(page)
```

### Use case: User inputs a search term and sees a list of relevant pages with titles and snippets

* The **Client** sends a request to the **Web Server**, running as a [reverse proxy](https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server)
* The **Web Server** forwards the request to the **Query API** server
* The **Query API** server does the following:
    * Parses the query
        * Removes markup
        * Breaks up the text into terms
        * Fixes typos
        * Normalizes capitalization
        * Converts the query to use boolean operations
    * Uses the **Reverse Index Service** to find documents matching the query
        * The **Reverse Index Service** ranks the matching results and returns the top ones (document ids)
    * Uses the **Document Service** to return titles and snippets

We'll use a public [**REST API**](https://github.com/donnemartin/system-design-primer#representational-state-transfer-rest):

```
$ curl https://search.com/api/v1/search?query=hello+world
```

Response:

```
{
    "title": "foo's title",
    "snippet": "foo's snippet",
    "link": "https://foo.com",
},
{
    "title": "bar's title",
    "snippet": "bar's snippet",
    "link": "https://bar.com",
},
{
    "title": "baz's title",
    "snippet": "baz's snippet",
    "link": "https://baz.com",
},
```

For internal communications, we could use [Remote Procedure Calls](https://github.com/donnemartin/system-design-primer#remote-procedure-call-rpc).

### Handling duplicates

We need to be careful the web crawler doesn't get stuck in an infinite loop, which happens when the graph contains a cycle.

#### option1: admission control (quota allocation)
set a limit on the frequency of crawling the site.
对于热门的网站，不能无限制的抓取，所以需要进行二级调度。首先调度抓取哪个网站，然后选中了要抓取的网站之后，调度在该网站中抓取哪些网页。这样做的好处是，非常礼貌的对单个网站的抓取有一定的限制，也给其他网站的网页抓取一些机会

#### option2 remove duplicate urls

* For smaller lists we could use something like `sort | unique`
* With 1 billion links to crawl, we could use **MapReduce** to output only entries that have a frequency of 1

```
class RemoveDuplicateUrls(MRJob):

    def mapper(self, _, line):
        yield line, 1

    def reducer(self, key, values):
        total = sum(values)
        if total == 1:
            yield key, total
```

Detecting duplicate content is more complex.  We could generate a signature based on the contents of the page and compare those two signatures for similarity.  Some potential algorithms are [Jaccard index](https://en.wikipedia.org/wiki/Jaccard_index) and [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity).

### Determining when to update the crawl results

Pages need to be crawled regularly to ensure freshness.  Crawl results could have a `timestamp` field that indicates the last time a page was crawled.  After a default time period, say one week, all pages should be refreshed.  Frequently updated or more popular sites could be refreshed in shorter intervals.

#### Option1: analytics
Although we won't dive into details on analytics, we could do some data mining to determine the mean time before a particular page is updated, and use that statistic to determine how often to re-crawl the page.

We might also choose to support a `Robots.txt` file that gives webmasters control of crawl frequency.

#### Option2: exponential back-off
Exponential back-off!

success: set available time to 1 week later -> if found updated -> 0.5 week later -> 0.25 week later ... -> 1min -> not updated ? -> 2min -> 4min

failure: set to 1 week later -> found failure -> 2Week later -> 4 -> 8week later

对于更新快的网页分配的资源越来越多，对于更新慢或者失效的网页分配的资源越来越少

## Step 4: Scale the design

> Identify and address bottlenecks, given the constraints.

![Imgur](http://i.imgur.com/bWxPtQA.png)

### Motivation

* large number of queries can't be handle by a single webserver
* queries are not evenly distributed
* crawler service can be slow down by performing dns look up

### How to scale

Some searches are very popular, while others are only executed once.  Popular queries can be served from a **Memory Cache** such as Redis or Memcached to reduce response times and to avoid overloading the **Reverse Index Service** and **Document Service**.  The **Memory Cache** is also useful for handling the unevenly distributed traffic and traffic spikes.  

Below are a few other optimizations to the **Crawling Service**:

* To handle the data size and request load, the **Reverse Index Service** and **Document Service** will likely need to make heavy use sharding and replication.
* DNS lookup can be a bottleneck, the **Crawler Service** can keep its own DNS lookup that is refreshed periodically
* The **Crawler Service** can improve performance and reduce memory usage by keeping many open connections at a time, referred to as [connection pooling](https://en.wikipedia.org/wiki/Connection_pool)
    * Switching to [UDP](https://github.com/donnemartin/system-design-primer#user-datagram-protocol-udp) could also boost performance
* Web crawling is bandwidth intensive, ensure there is enough bandwidth to sustain high throughput

## Additional talking points

> Additional topics to dive into, depending on the problem scope and time remaining.


### Asynchronism and microservices

* [Message queues](https://github.com/donnemartin/system-design-primer#message-queues)
* [Task queues](https://github.com/donnemartin/system-design-primer#task-queues)
* [Back pressure](https://github.com/donnemartin/system-design-primer#back-pressure)
* [Microservices](https://github.com/donnemartin/system-design-primer#microservices)
