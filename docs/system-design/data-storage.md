[Big Table](http://blog.bittiger.io/post175/)
[google onsite question](https://www.jiuzhang.com/qa/627/)

# Data storage & retrieval
![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch03-map-ebook.png)
![2](https://cdn-images-1.medium.com/max/2000/1*Yp10mfavInjDULz5Qz-f-Q.png)
![3](https://cdn-images-1.medium.com/max/2000/1*cwUuBS3Z_sZK19R0ig5zEA.png)
![4](https://cdn-images-1.medium.com/max/2000/1*iI7vzaOjFWWwZKtTaJCtXQ.png)

Storage engines fall into 2 categories:

1. OLTP (transaction processing)
    - typically user-facing
    - huge volume of requests/queries
    - each query only touchs a small # of records
    - storage engine uses an index to find the data for the requested key
    - disk seek time is the bottleneck

2. OLAP (analytics)
    - used in data warehouses & analytic system
    - used by business analysts, not end users
    - handle a much lower volume of queries than OLTP
    - each query is very demanding, scanning millions of records in a short time
    - disk bandwith (not seek time) is the bottleneck
    - column-oriented storage is popular

on the OLTP side, two schools of storage engine differ in the way they build `indexes`.

1. The log-structured school
    - only permits appending to files and deleting obsolete files
    - never updates a file that has been written
    - systematically turn random-access writes into sequential writes on disk
    - enables higher write throughput due to performance characteristics of hard drives & SSDs.
    - SSTables, LSM-trees, Canssandra, Lucene

2. The update-in-place school
    - treats the disk as a set of fixed-size pages that can be overwritten
    - B-trees are being used in all major relational databases and also many nonrelational ones.

When your queries require sequentially scanning across a large number of rows, `indexes` are much less relevant. Instead it becomes important to encode data very compacty, to minimize the amount of data that the query needs to read from the disk. Column-oriented storage is designed for this purpose.

---

## world’s simplest database, implemented as two Bash functions
```
#!/bin/bash

db_set () {
    echo "$1,$2" >> database
}

db_get () {
    grep "^$1," database | sed -e "s/^$1,//" | tail -n 1
}
```

* underlying storage format: a text file where each line contains a key value pair , separated by a comma
* if you update a key several times, the old versions of the value are not overwritten
* you need to look at the last occurrence of a key in a file to find the latest value

### performance
* appending to a file is generally very efficient, so db_set is very fast
* db_get has terrible performance if you have large # of records in your db
* the cost of look up in O(n).

In order to efficiently find the value for a particular key in the database, we need a different data structure: an index.

Maintaining additional structures incurs overhead, especially on writes.

## in memory hashtable
![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0301.png)

* used by `Bitcask`
* the simplest possible indexing strategy is this: keep an in-memory hash map where every key is mapped to a byte offset in the data file

### storage engine work flow
* whenever you append a new key-value pair to the file, you also update the hash map to reflect the offset of the data you just wrote (this works both for inserting new keys and for updating existing keys)
* When you want to look up a value, use the hash map to find the offset in the data file, seek to that location, and read the value

### pros & cons
* pros
    * high-performance reads and writes
    * The values can use more space than there is available memory, since they can be loaded from disk with just one disk seek. If that part of the data file is already in the filesystem cache, a read doesn’t require any disk I/O at all.
    * well suited to situations where the value for each key is updated frequently, and there are limited number of distinct keys
      * the number of times a youtube video has been played
      * the number of likes you received from your post
* cons
    * all the keys fit in the available RAM, since the hash map is kept completely in memory
    * eventually running out of disk by appending forever

## in mem hashtable + compacted segment

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0302.png)
![2](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0303.png)

### storage engine work flow
* break the log into segments of a certain size by closing a segment file when it reaches a certain size, and making subsequent writes to a new segment file.
* We can then perform compaction on these segments, throwing away duplicate keys in the log, and keeping only the most recent update for each key.
* since compaction often makes segments much smaller (assuming that a key is overwritten several times on average within one segment), we can also merge several segments together at the same time as performing the compaction
* The merging and compaction of frozen segments can be done in a background thread, and while it is going on, we can still continue to serve read and write requests as normal, using the old segment files.
* After the merging process is complete, we switch read requests to using the new merged segment instead of the old segments—and then the old segment files can simply be deleted.
* Each segment now has its own in-memory hash table, mapping keys to file offsets. In order to find the value for a key, we first check the most recent segment’s hash map; if the key is not present we check the second-most-recent segment, and so on.
* The merging process keeps the number of segments small, so lookups don’t need to check many hash maps.

### some details to make Bitcask-like

* Deleting records
    * If you want to delete a key and its associated value, you have to append a special deletion record to the data file (sometimes called a tombstone). When log segments are merged, the tombstone tells the merging process to discard any previous values for the deleted key.
* Crash recovery
    * If the database is restarted, the in-memory hash maps are lost. In principle, you can restore each segment’s hash map by reading the entire segment file from beginning to end and noting the offset of the most recent value for every key as you go along. However, that might take a long time if the segment files are large, which would make server restarts painful. Bitcask speeds up recovery by storing a snapshot of each segment’s hash map on disk, which can be loaded into memory more quickly.
* Partially written records
    * The database may crash at any time, including halfway through appending a record to the log. Bitcask files include checksums, allowing such corrupted parts of the log to be detected and ignored.
* Concurrency control
    * As writes are appended to the log in a strictly sequential order, a common implementation choice is to have only one writer thread. Data file segments are append-only and otherwise immutable, so they can be read concurrently by multiple threads.

### pros & cons
* pros
    * Sequential write operation
        * Appending and segment merging are sequential write operations, which are generally much faster than random writes, especially on magnetic spinning-disk hard drives.
    * Concurrency and crash recovery
        * Concurrency and crash recovery are much simpler if segment files are append-only or immutable. For example, you don’t have to worry about the case where a crash happened while a value was being overwritten, leaving you with a file containing part of the old and part of the new value spliced together.
    * fragmentation
        * Merging old segments avoids the problem of data files getting fragmented over time.
* cons
    * The hash table must fit in memory, so if you have a very large number of keys, you’re out of luck.
    * Range queries are not efficient. Hash is not good at range queries, you’d have to look up each key individually in the hash maps.

## SSTables & LSM-Trees

SSTables have several big advantages over log segments with hash indexes by  making a simple change to the format of our segment files: we require that the sequence of key-value pairs is sorted by key. It also requires that each key only appears once within each merged segment file (the compaction process already ensures that).

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0304.png)

* Merging segments is simple and efficient
    * The approach is like the one used in the mergesort algorithm. you start reading the input files side by side, look at the first key in each file, copy the lowest key (according to the sort order) to the output file, and repeat. This produces a new merged segment file, also sorted by key.
    * When multiple segments contain the same key, we can keep the value from the most recent segment and discard the values in older segments.

![2](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0305.png)

* You no longer need to keep an index of all the keys in memory.
    * even if the key is not in the sparse index, you can use binary search to find the two boundary keys and start searching from the lower bound to upperbound key.
    * You still need an in-memory index to tell you the offsets for some of the keys, but it can be sparse: one key for every few kilobytes of segment file is sufficient, because a few kilobytes can be scanned very quickly
    * 每个SSTable配置一个sparse index

* compression also reduces the I/O bandwidth use
    * Since read requests need to scan over several key-value pairs in the requested range anyway, it is possible to group those records into a block and compress it before writing it to disk

### How do you get data to by sorted in each SSTable

Maintaining a sorted structure on disk is possible (see “B-Trees”), but maintaining it in memory is much easier. There are plenty of well-known tree data structures that you can use, such as red-black trees or AVL trees [2]. With these data structures, you can insert keys in any order and read them back in sorted order.

### Storage engine work flow

* When a write comes in, add it to an in-memory balanced tree data structure (for example, a red-black tree). This in-memory tree is sometimes called a memtable.

* When the memtable gets bigger than some threshold—typically a few megabytes—write it out to disk as an SSTable file. This can be done efficiently because the tree already maintains the key-value pairs sorted by key. The new SSTable file becomes the most recent segment of the database. While the SSTable is being written out to disk, writes can continue to a new memtable instance.

* In order to serve a read request, first try to find the key in the memtable, then in the most recent on-disk segment, then in the next-older segment, etc.

* From time to time, run a merging and compaction process in the background to combine segment files and to discard overwritten or deleted values.

### crash recovery

This scheme works very well. It only suffers from one problem: if the database crashes, the most recent writes (which are in the memtable but not yet written out to disk) are lost. In order to avoid that problem, we can keep a separate log on disk to which every write is immediately appended, just like in the previous section. That log is not in sorted order, but that doesn’t matter, because its only purpose is to restore the memtable after a crash. Every time the memtable is written out to an SSTable, the corresponding log can be discarded.

### Who is using LSM-Tree

Originally this indexing structure was described by Patrick O’Neil et al. under the name Log-Structured Merge-Tree (or LSM-Tree) [10], building on earlier work on log-structured filesystems [11]. Storage engines that are based on this principle of merging and compacting sorted files are often called LSM storage engines.

the basic idea of LSM-trees—keeping a cascade of SSTables that are merged in the background—is simple and effective.

Even when the dataset is much bigger than the available memory it continues to work well.

Since data is stored in sorted order, you can efficiently perform range queries (scanning all keys above some minimum and up to some maximum), and because the disk writes are sequential the LSM-tree can support remarkably high write throughput.


* LevelDB, RocksDB
* HBase & Cassandra
* Google BigTable
* Lucene, an indexing engine for full-text search used by Elasticsearch and Solr
    * A full-text index is much more complex than a key-value index but is based on a similar idea: given a word in a search query, find all the documents (web pages, product descriptions, etc.) that mention the word.
    * This is implemented with a key-value structure where the key is a word (a term) and the value is the list of IDs of all the documents that contain the word (the postings list).
    * In Lucene, this mapping from term to postings list is kept in SSTable-like sorted files, which are merged in the background as needed

### pros & cons

* cons
    * the LSM-tree algorithm can be slow when looking up keys that do not exist in the database
    * you have to check the memtable, then the segments all the way back to the oldest (possibly having to read from disk for each one) before you can be sure that the key does not exist.
    * In order to optimize this kind of access, storage engines often use additional Bloom filters
    * A Bloom filter is a memory-efficient data structure for approximating the contents of a set. It can tell you if a key does not appear in the database, and thus saves many unnecessary disk reads for nonexistent keys

## B-Trees

Like SSTables, B-trees keep key-value pairs sorted by key, which allows efficient key-value lookups and range queries. But that’s where the similarity ends: B-trees have a very different design philosophy.

The log-structured indexes we saw earlier break the database down into variable-size segments, typically several megabytes or more in size, and always write a segment sequentially. By contrast, B-trees break the database down into fixed-size blocks or pages, traditionally 4 KB in size (sometimes bigger), and read or write one page at a time. This design corresponds more closely to the underlying hardware, as disks are also arranged in fixed-size blocks.

Each page can be identified using an address or location, which allows one page to refer to another—similar to a pointer, but on disk instead of in memory. We can use these page references to construct a tree of pages

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0306.png)

One page is designated as the root of the B-tree; whenever you want to look up a key in the index, you start here. The page contains several keys and references to child pages. Each child is responsible for a continuous range of keys, and the keys between the references indicate where the boundaries between those ranges lie.

We are looking for the key 251, so we know that we need to follow the page reference between the boundaries 200 and 300. That takes us to a similar-looking page that further breaks down the 200–300 range into subranges. Eventually we get down to a page containing individual keys (a leaf page), which either contains the value for each key inline or contains references to the pages where the values can be found.

The number of references to child pages in one page of the B-tree is called the branching factor. In practice, the branching factor depends on the amount of space required to store the page references and the range boundaries, but typically it is several hundred.

This algorithm ensures that the tree remains balanced: a B-tree with n keys always has a depth of O(log n). Most databases can fit into a B-tree that is three or four levels deep, so you don’t need to follow many page references to find the page you are looking for. (A four-level tree of 4 KB pages with a branching factor of 500 can store up to 256 TB.)

### Making B-Trees reliable

* Crash recovery
    * some operations require several different pages to be overwritten. For example, if you split a page because an insertion caused it to be overfull, you need to write the two pages that were split, and also overwrite their parent page to update the references to the two child pages. This is a dangerous operation, because if the database crashes after only some of the pages have been written, you end up with a corrupted index (e.g., there may be an orphan page that is not a child of any parent).

    * In order to make the database resilient to crashes, it is common for B-tree implementations to include an additional data structure on disk: a write-ahead log (WAL, also known as a redo log). This is an append-only file to which every B-tree modification must be written before it can be applied to the pages of the tree itself. When the database comes back up after a crash, this log is used to restore the B-tree back to a consistent state.

* Concurrency control
    * An additional complication of updating pages in place is that careful concurrency control is required if multiple threads are going to access the B-tree at the same time—otherwise a thread may see the tree in an inconsistent state.
    * This is typically done by protecting the tree’s data structures with latches (lightweight locks). Log-structured approaches are simpler in this regard, because they do all the merging in the background without interfering with incoming queries and atomically swap old segments for new segments from time to time.

### B-Tree Optimization

* Copy on write
    * instead of overwriting pages and maintaining a WAL for crash recovery, some databases (like LMDB) use a copy-on-write scheme. A modified page is written to a different location, and a new version of the parent pages in the tree is created, pointing at the new location. This approach is also useful for concurrency control, as we shall see in “Snapshot Isolation and Repeatable Read”.

* Abbreviate keys
    * We can save space in pages by not storing the entire key, but abbreviating it. Especially in pages on the interior of the tree, keys only need to provide enough information to act as boundaries between key ranges. Packing more keys into a page allows the tree to have a higher branching factor, and thus fewer level

* Pointers to siblings
    * Additional pointers have been added to the tree. For example, each leaf page may have references to its sibling pages to the left and right, which allows scanning keys in order without jumping back to parent pages.

## Compare B-Tree to LSM Trees

* LSM-trees
    * pros
        * faster for writes
        * LSM-trees are typically able to sustain higher write throughput than B-trees, partly because they sequentially write compact SSTable files rather than having to overwrite several pages in the tree
        * LSM-trees has less write amplification than Btree
        * LSM-trees can be compressed better, and thus often produce smaller files on disk than B-trees. LSM-trees are not page-oriented and periodically rewrite SSTables to remove fragmentation, they have lower storage overheads, especially when using leveled compaction.
    * cons
        * reads are slower because they have to check several different data structures and SSTables at different stages of compaction
        * Log-structured indexes also rewrite data multiple times due to repeated compaction and merging of SSTables
        * compaction process can sometimes interfere with the performance of ongoing reads and writes. disks have limited resources, so it can easily happen that a request needs to wait while the disk finishes an expensive compaction operation.
        * If write throughput is high and compaction is not configured carefully, it can happen that compaction cannot keep up with the rate of incoming writes. In this case, the number of unmerged segments on disk keeps growing until you run out of disk space, and reads also slow down because they need to check more segment files
* B-tree
    * pros
        * faster for reads
        * An advantage of B-trees is that each key exists in exactly one place in the index, whereas a log-structured storage engine may have multiple copies of the same key in different segments. This aspect makes B-trees attractive in databases that want to offer strong transactional semantics. in many relational databases, transaction isolation is implemented using locks on ranges of keys, and in a B-tree index, those locks can be directly attached to the tree.
    * cons
        * A B-tree index must write every piece of data at least twice: once to the write-ahead log, and once to the tree page itself (and perhaps again as pages are split).
        * There is also overhead from having to write an entire page at a time, even if only a few bytes in that page changed.
        * B-tree storage engines leave some disk space unused due to fragmentation: when a page is split or when a row cannot fit into an existing page, some space in a page remains unused

## Secondary Indexes
A secondary index can easily be constructed from a key-value index. The main difference is that keys are not unique; i.e., there might be many rows (documents, vertices) with the same key. This can be solved in two ways: either by making each value in the index a list of matching row identifiers (like a postings list in a full-text index) or by making each key unique by appending a row identifier to it. Either way, both B-trees and log-structured indexes can be used as secondary indexes.

The key in an index is the thing that queries search for, but the value can be one of two things: it could be the actual row (document, vertex) in question, or it could be a reference to the row stored elsewhere.

### Heap file approach
In the latter case, the place where rows are stored is known as a heap file, and it stores data in no particular order (it may be append-only, or it may keep track of deleted rows in order to overwrite them with new data later). The heap file approach is common because it avoids duplicating data when multiple secondary indexes are present: each index just references a location in the heap file, and the actual data is kept in one place

When updating a value without changing the key, the heap file approach can be quite efficient: the record can be overwritten in place, provided that the new value is not larger than the old value.

The situation is more complicated if the new value is larger, as it probably needs to be moved to a new location in the heap where there is enough space. In that case, either all indexes need to be updated to point at the new heap location of the record, or a forwarding pointer is left behind in the old heap location

### Clustered index
In some situations, the extra hop from the index to the heap file is too much of a performance penalty for reads, so it can be desirable to store the indexed row directly within an index. This is known as a clustered index. For example, in MySQL’s InnoDB storage engine, the primary key of a table is always a clustered index, and secondary indexes refer to the primary key (rather than a heap file location)  In SQL Server, you can specify one clustered index per table.

## Muti-column indexes (geospatial database)
Multi-dimensional indexes are a more general way of querying several columns at once, which is particularly important for geospatial data

```
#!/bin/bash
SELECT * FROM restaurants WHERE latitude  > 51.4946 AND latitude  < 51.5079
                            AND longitude > -0.1162 AND longitude < -0.1004;
```

A standard B-tree or LSM-tree index is not able to answer that kind of query efficiently: it can give you either all the restaurants in a range of latitudes (but at any longitude), or all the restaurants in a range of longitudes (but anywhere between the North and South poles), but not both simultaneously.

An interesting idea is that multi-dimensional indexes are not just for geographic locations. For example, on an ecommerce website you could use a three-dimensional index on the dimensions (red, green, blue) to search for products in a certain range of colors, or in a database of weather observations you could have a two-dimensional index on (date, temperature) in order to efficiently search for all the observations during the year 2013

## Full-text search and fuzzy indexes
All the indexes discussed so far assume that you have exact data and allow you to query for exact values of a key, or a range of values of a key with a sort order. What they don’t allow you to do is search for similar keys, such as misspelled words. Such fuzzy querying requires different techniques.

Lucene is able to search text for words within a certain edit distance (an edit distance of 1 means that one letter has been added, removed, or replaced)

Lucene uses a SSTable-like structure for its term dictionary. This structure requires a small in-memory index that tells queries at which offset in the sorted file they need to look for a key. In LevelDB, this in-memory index is a sparse collection of some of the keys, but in Lucene, the in-memory index is a finite state automaton over the characters in the keys, similar to a trie. This automaton can be transformed into a Levenshtein automaton, which supports efficient search for words within a given edit distance

## In memory data store
The data structures discussed so far in this chapter have all been answers to the limitations of disks. Compared to main memory, disks are awkward to deal with.

However, we tolerate this awkwardness because disks have two significant advantages: they are durable (their contents are not lost if the power is turned off), and they have a lower cost per gigabyte than RAM.

As RAM becomes cheaper, the cost-per-gigabyte argument is eroded. Many datasets are simply not that big, so it’s quite feasible to keep them entirely in memory, potentially distributed across several machines. This has led to the development of in-memory databases.

Some in-memory key-value stores, such as Memcached, are intended for caching use only, where it’s acceptable for data to be lost if a machine is restarted. But other in-memory databases aim for durability, which can be achieved with special hardware (such as battery-powered RAM), by writing a log of changes to disk, by writing periodic snapshots to disk, or by replicating the in-memory state to other machines.

Counterintuitively, the performance advantage of in-memory databases is not due to the fact that they don’t need to read from disk.  Even a disk-based storage engine may never need to read from disk if you have enough memory, because the operating system caches recently used disk blocks in memory anyway. Rather, they can be faster because they can avoid the overheads of encoding in-memory data structures in a form that can be written to disk.

## why some NoSQL db drops join ?

一开始我以为是不同的storage engine导致的，但是仔细想想，其实join不过只是针对不同的key做range query之后进行的merge result而已。所以NoSQL之所以不去实现join是因为NoSQL主要目标是分布式环境，当database scale到分布式节点上的时候，join就很难进行了，所以干脆不支持，让数据denormolized。

JOINs are important because they allow you to maintain a single source of truth and access disparate data easily.

In theory, a JOIN allows me to connect any piece of data in the DB to any other related piece of data by simply connecting the tables. This means that I can create a fully normalized structure and store each piece of data exactly once in exactly one place. i.e. a fully normalized database

A nice side effect of this is that I don't have to worry about things like synchronizing the data. There is only one entry and one source of truth. The numbers returned from a given query are "as correct" as they can be.

The other side effect is that I can query data from disparate parts of the system and bring them together in ways that I may not have planned for in advance.

The key problem here is that JOINs don't scale very well across multiple computers. It can be done, but it's hard and not easy to generalize. Most "Document-oriented" databases specifically want to scale across multiple computers. So they just drop the JOINs and a few other querying features and suddenly scaling across multiple nodes becomes dramatically easier.

But then you also lose those nice side effects I listed above.

There's a trade-off here. SQL is dramatically more powerful than most of the query languages for Document-oriented databases. But SQL has problems / becomes expensive beyond a single node.

Some "NoSQL" database do have joins. In fact Graph databases are explicitly good at doing joins. There's also a world of "Object Databases" that typically support some form of join as well.

## why some NoSQL not supporting secondary index
也是因为在分布式环境下 secondary index不好实现吧。
see [partition](./partitioning.md)
