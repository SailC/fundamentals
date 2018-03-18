# cache

## cache的作用
![1](https://camo.githubusercontent.com/7acedde6aa7853baf2eb4a53f88e2595ebe43756/687474703a2f2f692e696d6775722e636f6d2f51367a32344c612e706e67)
Caching improves page load times and can reduce the load on your servers and databases. In this model, the dispatcher will first lookup if the request has been made before and try to find the previous result to return, in order to save the actual execution.

Databases often benefit from a uniform distribution of reads and writes across its partitions. Popular items can skew the distribution, causing bottlenecks. Putting a cache in front of a database can help absorb uneven loads and spikes in traffic.

## cache的种类

![1](https://tech.meituan.com/img/cache_about/%E7%BD%91%E7%BB%9C%E5%BA%94%E7%94%A8%E4%B8%80%E8%88%AC%E6%B5%81%E7%A8%8B.png)

缓存的使用可以出现在1～4的各个环节中，每个环节的缓存方案与使用各有特点

- client caching (客户机器上的browser, OS)
- server side
    - web server/ reverse proxy can serve static and dynamic content directly.
    - database usually includes some level of caching in a default configuration, optimized for a generic use case.
    - Application caching
        - In-memory caches such as Memcached and Redis are key-value stores between your application and your data storage.

## 如何cache

- cache at the database query level.
    - hash the query as a key and store the result to the cache.
    - cons
        - hard to delete a cached result with complex queries
        - if one piece of data change such as a table cell, you need to delete all cached queries that might include that cell
- cache at the object query level.
    - See your data as an object, similar to what you do with your application code
    - Have your application assemble the dataset from the database into a class instance or a data structure(s)
    - Remove the object from cache if its underlying data has changed
    - Allows for asynchronous processing: workers assemble objects by consuming the latest cached object

## cache什么

- User sessions
    * 用户是如何实现登陆与保持登陆的?
      * 用户 Login 以后 创建一个 session 对象
      * 并把 session_key 作为 cookie 值返回给浏览器
      * 浏览器将该值记录在浏览器的cookie 中
      * 用户每次向服务器发送的访问，都会自动带上该网站所有的 cookie
      * 此时服务器检测到cookie中的session_key是有效的，就认为用户登陆了
      * 用户 Logout 之后 从 session table 里删除对应数据
      * session table = session key + user id + expire_at
- Fully rendered web pages
- Activity streams
- User graph data

## eviction policy

Kick out the following entry when the cache is full.

RAM is more limited than disk, so cache invalidation algorithms such as least recently used (LRU) can help invalidate 'cold' entries and keep 'hot' data in RAM.

- FIFO(first in first out)
    - 先进先出策略，最先进入缓存的数据在缓存空间不够的情况下（超出最大元素限制）会被优先被清除掉，以腾出新的空间接受新的数据。策略算法主要比较缓存元素的创建时间。
    - 在数据实效性要求场景下可选择该类策略，优先保障最新数据可用。

- [LRU](https://leetcode.com/problems/lru-cache/description/): Least recent used
    - hashtable for hashing + doubly linked list for recency order
    - 在热点数据场景下较适用，优先保证热点数据的有效性

- [LFU](https://leetcode.com/problems/lfu-cache/description/): Least frequently used
    - a complicated one
    - 在保证高频数据有效性场景下，可选择这类策略。

- [Windowed LFU]
    - LFU会把过去常常被访问的过气entry保留下来，这是不合时宜的
    - maintain a window, only the cnts inside the window matters

## invalidation policy

### cache through `redis`
client only talk to cache, cache & db interactions are transparent to the client

```
  def set_user(user_id, values):
  user = db.query("UPDATE Users WHERE id = {0}", user_id, values)
  cache.set(user_id, user)
```

- write
    - write to db, and write to cache synchronously
- read
    - miss, cache will read value from db to cache, and return the value
    - hit, return the read value from cache directly
- pros
    - synchronous write operation makes the cache & db consistent
    - lower read latency since the newest update is usually in the cache due to the synchronous write, which increase the cache hit opportunities
    - Users are generally more tolerant of latency when updating data than reading data.
- cons
    - synchronous write also incurs higher write latency

### write back/behind
client only talk to cache, cache & db interactions are transparent to the client.
But cache & db interactions are asynchronous.

- write
    - write to cache, and cache can update the db asynchronously (or even group the updates and last write wins)
    > 当Laddy gaga 发新推文的时候，很多用户like,comment,造成同一条推文反复修改； 当采用WT 模式的时候，推文直接在cache 里面修改，立即返回用户，然后cache 在DB 不忙的时候再更新DB； 这样就降低了latancy ，并且减少了 DB峰值压力。
- pros
    - lower write latency due to asynchronous write operation
    - allievate the pressure on cache / db bandwith by grouping the operation
- cons (asynchronous -> bad consistency & durability)
    - data can be inconsistent between cache & db due to asynchronous write
    - read latency can increase due to more cache miss result by the asynchronous write
    - There could be data loss if the cache goes down prior to its contents hitting the data store.
    - It is more complex to implement write-behind than it is to implement cache-aside or write-through.

### cache aside
client directly talk to cache & db.

```
def get_user(self, user_id):
user = cache.get("user.{0}", user_id)
if user is None:
  user = db.query("SELECT * FROM users WHERE user_id = {0}", user_id)
  if user is not None:
      key = "user.{0}".format(user_id)
      cache.set(key, json.dumps(user))
return user
```

- write
    - client writes to db, and client invalids the cache entry
        - why invalid instead of update the entry ? because invalidation is indempotent, which is good for concurrent operations. if two updates happen concurrent, then there's race condition, and the last one that writes to db & cache determines the value there. So db & cache may be left in inconsistent state.
- read
    - hit, return the value from cache directly
      - miss, client read the db, and client put the value to cache

- pros
    - Cache-aside is also referred to as lazy loading. Only requested data is cached, which avoids filling up the cache with data that isn't requested.
- cons
    - Each cache miss results in three trips, which can cause a noticeable delay.
    - stale data (read cache miss -> get db value -> gc ... 此时db被更新了, -> gc 回来update cache导致 数据过期 -> lease)
    - thundering herds (对某个key产生巨大读写流量，写导致cache invalid，导致读cache miss，然后大量的traffic涌向db -> lease + window + slightly stale)

---

## 缓存分类和应用场景
缓存有各类特征，而且有不同介质的区别，那么实际工程中我们怎么去对缓存分类呢？在目前的应用服务框架中，比较常见的，时根据缓存雨应用的藕合度，分为local cache（本地缓存）和remote cache（分布式缓存）：

本地缓存：指的是在应用中的缓存组件，其最大的优点是应用和cache是在同一个进程内部，请求缓存非常快速，没有过多的网络开销等，在单应用不需要集群支持或者集群情况下各节点无需互相通知的场景下使用本地缓存较合适；同时，它的缺点也是应为缓存跟应用程序耦合，多个应用程序无法直接的共享缓存，各应用或集群的各节点都需要维护自己的单独缓存，对内存是一种浪费。
为了解决本地缓存数据的实时性问题，目前大量使用的是结合ZooKeeper的自动发现机制，实时变更本地静态变量缓存：

分布式缓存：指的是与应用分离的缓存组件或服务，其最大的优点是自身就是一个独立的应用，与本地应用隔离，多个应用可直接的共享缓存。

目前各种类型的缓存都活跃在成千上万的应用服务中，还没有一种缓存方案可以解决一切的业务场景或数据类型，我们需要根据自身的特殊场景和背景，选择最适合的缓存方案。缓存的使用是程序员、架构师的必备技能，好的程序员能根据数据类型、业务场景来准确判断使用何种类型的缓存，如何使用这种缓存，以最小的成本最快的效率达到最优的目的。

---

## distributed cache

What happens when you expand this to many nodes? If the request layer is expanded to multiple nodes, it’s still quite possible to ask each node to have a cache for the same contents. However, if your load balancer randomly distributes requests across the nodes, the same request will go to different nodes, thus increasing cache misses. Two choices for overcoming this hurdle are global caches and distributed caches.


In a distributed cache, each of its nodes own part of the cached data. Typically, the cache is divided up using a consistent hashing function, such that if a request node is looking for a certain piece of data, it can quickly know where to look within the distributed cache to determine if that data is available. In this case, each node has a small piece of the cache, and will then send a request to another node for the data before going to the origin. Therefore, one of the advantages of a distributed cache is the ease by which we can increase the cache space, which can be achieved just by adding nodes to the request pool.

A disadvantage of distributed caching is resolving a missing node. Some distributed caches get around this by storing multiple copies of the data on different nodes; however, you can imagine how this logic can get complicated quickly, especially when you add or remove nodes from the request layer. Although even if a node disappears and part of the cache is lost, the requests will just pull from the origin—so it isn’t necessarily catastrophic!

cache的分布式主要是在客户端实现，通过客户端的路由处理来达到分布式解决方案的目的。客户端做路由的原理非常简单，应用服务器在每次存取某key的value时，通过某种算法把key映射到某台memcached服务器nodeA上，因此这个key所有操作都在nodeA上，结构图如图6、图7所示。

![6](https://tech.meituan.com/img/cache_about/memcached%E5%AE%A2%E6%88%B7%E7%AB%AF%E8%B7%AF%E7%94%B1%E5%9B%BE.png)
![7](https://tech.meituan.com/img/cache_about/memcached%E4%B8%80%E8%87%B4%E6%80%A7hash%E7%A4%BA%E4%BE%8B%E5%9B%BE.png)

memcached客户端采用一致性hash算法作为路由策略，如图7，相对于一般hash（如简单取模）的算法，一致性hash算法除了计算key的hash值外，还会计算每个server对应的hash值，然后将这些hash值映射到一个有限的值域上（比如0~2^32）。通过寻找hash值大于hash(key)的最小server作为存储该key数据的目标server。如果找不到，则直接把具有最小hash值的server作为目标server。同时，一定程度上，解决了扩容问题，增加或删除单个节点，对于整个集群来说，不会有大的影响。最近版本，增加了虚拟节点的设计，进一步提升了可用性。

memcached是一个高效的分布式内存cache，了解memcached的内存管理机制，才能更好的掌握memcached，让我们可以针对我们数据特点进行调优，让其更好的为我所用。我们知道memcached仅支持基础的key-value键值对类型数据存储。在memcached内存结构中有两个非常重要的概念：slab和chunk。如图8所示。

---

## reference
- https://tech.meituan.com/cache_about.html
- https://www.youtube.com/watch?v=6phA3IAcEJ8
