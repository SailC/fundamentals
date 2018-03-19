
# distributed id generator

## Problem & Features

---

Many complicated distributed systems need to uniquely identify the data or message. The typical solution that works for a single database — just using a database’s natural auto-incrementing primary key feature — no longer works when data is being inserted into many databases at the same time.

## Functional Requirements:

---

1. globally unique:
    - can't have duplicated id for different data item
2. incremental id
    - since most RDBMS uses B-tree to index the data, use incremental primary key to get better performance when creating index.

3.  sortable by time (so a list of photo IDs, for example, could be sorted without fetching more information about the photos)

4.  IDs should ideally be 64 bits (for smaller indexes, and better storage in systems like Redis)

## Extra Requirements:

---

1. High availability (if Id generator system is unavaliable , new data item can't be inserted to the data base, which can be a disaster)
1. Low latency
1. High QPS

## why not simply use local program to generate ids?

1. UUID is local algorithm, but some of them have no order
2. use current time (in ms), can afford only up to 1000 concurrent calls.

UUID(Universally Unique Identifier)的标准型式包含32个16进制数字，以连字号分为五段，形式为8-4-4-4-12的36个字符，示例：550e8400-e29b-41d4-a716-446655440000

* 优点：
    * 性能非常高：本地生成，没有网络消耗。
* 缺点：
  * 不易于存储：UUID太长，16字节128位，通常以36长度的字符串表示，很多场景不适用。
  * 信息不安全：基于MAC地址生成UUID的算法可能会造成MAC地址泄露，这个漏洞曾被用于寻找梅丽莎病毒的制作者位置。
  * ID作为主键时在特定的环境会存在一些问题，比如做DB主键的场景下，UUID就非常不适用：
      * MySQL官方有明确的建议主键要尽量越短越好[4]，36个字符长度的UUID不符合要求。
      * 对MySQL索引不利：如果作为数据库主键，在InnoDB引擎下，UUID的无序性可能会引起数据位置频繁变动，严重影响性能。

> All indexes other than the clustered index are known as secondary indexes. In InnoDB, each record in a secondary index contains the primary key columns for the row, as well as the columns specified for the secondary index. InnoDB uses this primary key value to search for the row in the clustered index. If the primary key is long, the secondary indexes use more space, so it is advantageous to have a short primary key.

---

## I : Generate IDs in web application

This approach leaves ID generation entirely up to your application, and not up to the database at all. For example, MongoDB’s ObjectId, which is 12 bytes long and encodes the timestamp as the first component. Another popular approach is to use UUIDs.

    UUID uuid = UUID.randomUUID();

- MongoDB provides an unique ObjectID for each data, this id consists of 4 parts:
    - 4 bytes of Unix timestamp
    - 3 bytes of machine id
    - 2 bytes of process id
    - 3 bytes of counter
- There are different implementations of the UUID algorithm.
- `Pros`  :
    - Each machine can generate IDs individually, distributed in nature, minimizing points of failure and contention for ID generation.
    - generated locally, no network latency, high performance.
    - If you use a timestamp as the first component of the IDs, the IDs remain time-sortable
- `Cons`  :
    - Generally requires more storage space (96 bits or higer) to make reasonable uniqueness guarantees:
        - In InnoDB, each record in a secondary index contains the primary key columns for the row, as well as the columns specified for the secondary index. InnoDB uses this primary key value to search for the row in the clustered index. If the primary key is long, the secondary indexes use more space, so it is advantageous to have a short primary key.
    - Security issue. The UUID algorithm based on MAC address can expose MAC address to attackers.
    - Some UUID types are completely random and have no sorted nature, which is bad to be used as Primary Key :
        - UUID with no order can cause redordering of rows in the data blocks. (apart from the index entries being themselves sorted in the index block, primary index also enforces an ordering of rows in the data blocks.)
        - [What is difference between primary index and secondary index exactly? And what's advantage of one over another?](https://www.quora.com/What-is-difference-between-primary-index-and-secondary-index-exactly-And-whats-advantage-of-one-over-another/answer/Siddharth-Teotia?srid=nkLR)

## II: Database Ticket Server

![](https://static.notion-static.com/bc3b8bc9-76b1-452e-869a-f8fc6beb18bc/Untitled)

![](https://static.notion-static.com/0b371dc5-095b-4e2f-a8da-c6567dd9fa81/Untitled)

Uses the database’s auto-incrementing abilities to enforce uniqueness. Flickr uses this approach, but with two ticket DBs (one on odd numbers, the other on even) to avoid a single point of failure.

- MySQL has auto incremental ID, we can leverage that to construct a high performance distributed id generator.
- We can use 8 MySQL server. The first server is responsible for generating 1, 9, 17, 25 ... incrementing 8 at a time. The second sever is responsible for 2, 10, ... A load balancer can be used to route the request to the MySQL servers in a round-robin fashion.
- `Pros`
    - DBs are well understood and have pretty predictable scaling factors
- `Cons`
    - If using a single DB, becomes single point of failure. If using mutiple DBs, can no longer guarantee they they are sortable overtime(master down, slave promoted → inconsistent data). ids are not strictly monotonically increasing.
    - 数据库压力还是很大，每次获取ID都得读写一次数据库，只能靠堆机器来提高性能。
    - 系统水平扩展比较困难，比如定义好了步长和机器台数之后，如果要添加机器该怎么做？很难

## III: Generate IDs through dedicated service

Twitter’s Snowflake, a Thrift service that uses Apache ZooKeeper to coordinate nodes and then generates 64-bit unique IDs

![](https://static.notion-static.com/a7588734-5061-434c-aa2c-7a477afd21d0/Untitled)

Pros:

1. Snowflake IDs are 64-bits, half the size of a UUID
1. Can use time as first component and remain sortable
1. Distributed system can survive nodes dying

Cons:

1. introduce additional complexing and more `moving parts` (Zookeeper, Snowflake server) into our architecture.

 2.  heavily rely on machine clock,  machine clock moving backward will lead to duplicated IDs or available services.

## IV: DB ticket server with Snowflake-like algorithm

[Instagram](https://engineering.instagram.com/sharding-ids-at-instagram-1cf5a71e5a5c) combines approach III & IV.

- 41bit timestamp + 13 bit shard id (a shard is a PostgreSQL machine) + 10bit sequential id.
- Use existing ProstgreSQL cluster as a the DB ticket servers.

Our sharded system consists of several thousand ‘logical’ shards that are mapped in code to far fewer physical shards. Using this approach, we can start with just a few database servers, and eventually move to many more, simply by moving a set of logical shards from one database to another, without having to re-bucket any of our data. We used Postgres’ schemas feature to make this easy to script and administrate.

Schemas (not to be confused with the SQL schema of an individual table) are a logical grouping feature in Postgres. Each Postgres DB can h2have several schemas, each of which can contain one or more tables. Table names must only be unique per-schema, not per-DB, and by default Postgres places everything in a schema named ‘public’.

Each ‘logical’ shard is a Postgres schema in our system, and each sharded table (for example, likes on our photos) exists inside each schema.

We’ve delegated ID creation to each table inside each shard, by using PL/PGSQL, Postgres’ internal programming language, and Postgres’ existing auto-increment functionality.

Each of our IDs consists of:

41 bits for time in milliseconds (gives us 41 years of IDs with a custom epoch)
13 bits that represent the logical shard ID
10 bits that represent an auto-incrementing sequence, modulus 1024. This means we can generate 1024 IDs, per shard, per millisecond
Let’s walk through an example: let’s say it’s September 9th, 2011, at 5:00pm and our ‘epoch’ begins on January 1st, 2011. There have been 1387263000 milliseconds since the beginning of our epoch, so to start our ID, we fill the left-most 41 bits with this value with a left-shift:

`id = 1387263000 <<(64-41)`

Next, we take the shard ID for this particular piece of data we’re trying to insert. Let’s say we’re sharding by user ID, and there are 2000 logical shards; if our user ID is 31341, then the shard ID is 31341 % 2000 -> 1341. We fill the next 13 bits with this value:

`id |= 1341 <<(64-41-13)`

Finally, we take whatever the next value of our auto-increment sequence (this sequence is unique to each table in each schema) and fill out the remaining bits. Let’s say we’d generated 5,000 IDs for this table already; our next value is 5,001, which we take and mod by 1024 (so it fits in 10 bits) and include it too:

`id |= (5001 % 1024)`

We now have our ID, which we can return to the application server using the RETURNING keyword as part of the INSERT.

# Reference

[Leaf--美团点评分布式ID生成系统 -](https://tech.meituan.com/MT_Leaf.html)

[九章算法 - 帮助更多中国人找到好工作，硅谷顶尖IT企业工程师实时在线授课为你传授面试技巧](https://www.jiuzhang.com/article/gXM1xa/)

[Sharding & IDs at Instagram - Instagram Engineering](https://engineering.instagram.com/sharding-ids-at-instagram-1cf5a71e5a5c?gi=7093ee3fac31)

[常见分布式全局唯一ID生成策略及算法的对比](https://gavinlee1.github.io/2017/06/28/%E5%B8%B8%E8%A7%81%E5%88%86%E5%B8%83%E5%BC%8F%E5%85%A8%E5%B1%80%E5%94%AF%E4%B8%80ID%E7%94%9F%E6%88%90%E7%AD%96%E7%95%A5%E5%8F%8A%E7%AE%97%E6%B3%95%E7%9A%84%E5%AF%B9%E6%AF%94/)
