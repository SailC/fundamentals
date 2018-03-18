# Federation (vertical sharding)

比如你的 User Table 里有如下信息
* Email
* Username
* Password
* status_text // 签名
* avatar // 头像

我们知道 email / username / password 不会经常变动
* 而 status_text, avatar 相对来说变动频率更高
* 可以把他们拆分为两个表 User Table 和 User Profile Table
* 然后再分别放在两台机器上
* 这样如果 UserProfile Table 挂了，就不影响 User 正常的登陆

但是federation无法解决单个table过大的问题


# Partitioning (horizontal sharding)

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch06-map-ebook.png)

Partitioning is necessary when you have so much data that storing & processing it on a single machine is no longer feasible. The goal of partitioning is to spread the data and query load evenly across multiple machines, avoiding hot spots (nodes with disproportionately high load). By design, every partition operates mostly independently, and that allows a partitioned database to scale to multiple machines.

## Three approaches to partitioning

1. key range partitioning
    - keys are sorted
    - a partition owns a range of sorted keys
    - sorting enables efficient range queries
    - there is a risk of hot spot if app often accesses keys that are close in the sorted order
    - when a partition gets too big, it's usually rebalanced by splitting the range into two subranges

2. hash partitioning
    - a hash function is applied to each key
    - a partition owns a range of hashes
    - hashing destroys the ordering, making range queries inefficient
    - distribute the load more evenly
    - static partitioning v.s. dynamic partitioning
    - [rehashing](https://www.jiuzhang.com/solution/rehashing/)
        - 一般的数据库进行horizontal shard的方法是指，把 id 对 数据库服务器总数 n 取模，然后来得到他在哪台机器上。这种方法的缺点是，当数据继续增加，我们需要增加数据库服务器，将 n 变为 n+1 时，几乎所有的数据都要移动，这就造成了不 consistent。为了减少这种 naive 的 hash方法(%n) 带来的缺陷
    - [Consistent Hashing I](https://www.jiuzhang.com/solution/consistent-hashing/)
        - 将 id 对 360 取模，假如一开始有3台机器，那么让3台机器分别负责0~119, 120~239, 240~359 的三个部分。那么模出来是多少，查一下在哪个区间，就去哪台机器。
        当机器从 n 台变为 n+1 台了以后，我们从n个区间中，找到最大的一个区间，然后一分为二，把一半给第n+1台机器。
        比如从3台变4台的时候，我们找到了第3个区间0~119是当前最大的一个区间，那么我们把0~119分为0~59和60~119两个部分。0~59仍然给第1台机器，60~119给第4台机器。
        然后接着从4台变5台，我们找到最大的区间是第3个区间120~239，一分为二之后，变为 120~179, 180~239。
        在这个简单的版本有两个缺陷：
        * 增加一台机器之后，数据全部从其中一台机器过来，这一台机器的读负载过大，对正常的服务会造成影响。
        * 当增加到3台机器的时候，每台服务器的负载量不均衡，为1:1:2。
    - [Consistent Hashing II](https://www.jiuzhang.com/solution/consistent-hashing-ii/)
        - 将整个 Hash 区间看做环
        * 这个环的大小从 0~359 变为 0~2^64-1
        * 将机器和数据都看做环上的点
        * 引入 Micro shards / Virtual nodes 的概念
        * 一台实体机器对应 k 个 Micro shards / Virtual nodes
        * 每个 virtual node 对应 Hash 环上的一个点
        * 每新加入一台机器，就在环上随机撒 1000 个点作为 virtual nodes
        * 每个数据在圆周上也对应一个点，这个点通过一个 hash function 来计算。
        * 一个数据该属于那台机器负责管理，是按照该数据对应的圆周上的点在圆上顺时针碰到的第一个 micro-shard 点所属的机器来决定。
        * 新加入一台机器做数据迁移时
        * 1000 个 virtual nodes 各自向顺时针的一个 virtual node 要数据

3. hybrid partitioning
    - with a compund key
    - using one part of the key to identify the partition (sharding key)
    - another part of the key for range queries

## Consistent Hashing II


## Two methods for partitioning secondary index

1. Document-partitioned indexes (local indexes)
    - secondary indexes are stored in the same partition as the primary index
    - writes only update a single partition
    - reads requires a scatter/gather across all partitions

2. Term-partitioned indexes (global indexes)
    - secondary indexes are partitioned separately
    - an entry in the secondary index may include records from all partitions of the primary key
    - writes updates several partitions of the secondary index
    - reads can be served from a single partition

## Routing quries to the appropriate partition

1. partition-aware load balacing

2. parallel query execution engines
