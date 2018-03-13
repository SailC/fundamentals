# Partitioning

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

3. hybrid partitioning
    - with a compund key
    - using one part of the key to identify the partition (sharding key)
    - another part of the key for range queries

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
