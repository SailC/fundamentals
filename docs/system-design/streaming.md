# Stream Processing

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch11-map-ebook.png)

https://www.cloudamqp.com/blog/2014-12-03-what-is-message-queuing.html
https://stackoverflow.com/a/16019527

In some ways, stream processing is very much like the batch processing, but done continuously on unbounded (never-ending) streams rather than on a fixed-size input. From this perspective, message brokers and event logs serve as the streaming equivalent of a filesystem.

## two types of message brokers

1. AMQP/JMS-style message broker
    - The broker assigns individual messages to consumers, and consumers acknowledge individual messages when they have been successfully processed.
    - Messages are deleted from the broker once they have been acknowledged.
    - This approach is appropriate as an asynchronous form of RPC
    - the exact order of message processing is not preserved due to load balancing
    - you can't go back to read old messages again after they have been processed

2. Log-based message broker
    - The broker assigns all messages in a partition to the same consumer node, and always delivers messages in the same order.
    - Parallelism is achieved through partitioning
    - consumers track their progress by checkpointing the offset of the last message they have processed
    - The broker retains messages on disk, so it is possible to jump back and reread old messages if necessary.

The log-based approach has similarities to the replication logs found in databases and log-structured storage engines, this approach is especially appropriate for stream processing systems that consume input streams and generate derived state or derived output streams.

It can also be useful to think of the writes to a database as a stream: we can capture the changelog—i.e., the history of all changes made to a database—either implicitly through change data capture or explicitly through event sourcing. Log compaction allows the stream to retain a full copy of the contents of a database.

Representing databases as streams opens up powerful opportunities for integrating systems. You can keep derived data systems such as search indexes, caches, and analytics systems continually up to date by consuming the log of changes and applying them to the derived system. You can even build fresh views onto existing data by starting from scratch and consuming the log of changes from the beginning all the way to the present.

## purposes of stream processing

1. searching for event patterns

2. stream analytics

3. keeping derived data system up to date

we discussed techniques for achieving fault tolerance and exactly-once semantics in a stream processor. As with batch processing, we need to discard the partial output of any failed tasks. However, since a stream process is long-running and produces output continuously, we can’t simply discard all output. Instead, a finer-grained recovery mechanism can be used, based on microbatching, checkpointing, transactions, or idempotent writes.
