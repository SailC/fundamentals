# Data storage & retrieval
![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch03-map-ebook.png)

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
