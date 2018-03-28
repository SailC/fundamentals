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

---

Any kind of value-added transformation that can be done in real-time should be done as post-processing on the raw log feed produced. This would include things like `sessionization` of event data, or the addition of other derived fields that are of general interest. The original log is still available, but this real-time processing produces a derived log containing augmented data.

The typical approach to activity data in the web industry is to log it out to text files where it can be scrapped into a data warehouse or into Hadoop for aggregation and querying. The problem with this is the same as the problem with all batch ETL: it couples the data flow to the data warehouse's capabilities and processing schedule.

At LinkedIn, we have built our event data handling in a log-centric fashion. We are using Kafka as the central, multi-subscriber event log. We have defined several hundred event types, each capturing the unique attributes about a particular type of action. This covers everything from page views, ad impressions, and searches, to service invocations and application exceptions.

The "event-driven" style provides an approach to simplifying this. The job display page now just shows a job and records the fact that a job was shown along with the relevant attributes of the job, the viewer, and any other useful facts about the display of the job. Each of the other interested systems—the recommendation system, the security system, the job poster analytics system, and the data warehouse—all just subscribe to the feed and do their processing. The display code need not be aware of these other systems, and needn't be changed if a new data consumer is added.

### Scale the log

We used a few tricks in Kafka to support this kind of scale:

Partitioning the log
Optimizing throughput by batching reads and writes
Avoiding needless data copies

In order to allow horizontal scaling we chop up our log into partitions:

Each partition is a totally ordered log, but there is no global ordering between partitions

A log, like a filesystem, is easy to optimize for linear read and write patterns. The log can group small reads and writes together into larger, high-throughput operations. Kafka pursues this optimization aggressively. Batching occurs from client to server when sending data, in writes to disk, in replication between servers, in data transfer to consumers, and in acknowledging committed data.

### stream processing

The real driver for the processing model is the method of data collection. Data which is collected in batch is naturally processed in batch. When data is collected continuously, it is naturally processed continuously.

Seen in this light, it is easy to have a different view of stream processing: it is just processing which includes a notion of time in the underlying data being processed and does not require a static snapshot of the data so it can produce output at a user-controlled frequency instead of waiting for the "end" of the data set to be reached. In this sense, stream processing is a generalization of batch processing, and, given the prevalence of real-time data, a very important generalization.

### stateful real-time processing

Some real-time stream processing is just stateless record-at-a-time transformation, but many of the uses are more sophisticated counts, aggregations, or joins over windows in the stream. One might, for example, want to enrich an event stream (say a stream of clicks) with information about the user doing the click—in effect joining the click stream to the user account database. Invariably, this kind of processing ends up requiring some kind of state to be maintained by the processor: for example, when computing a count, you have the count so far to maintain. How can this kind of state be maintained correctly if the processors themselves can fail?

Some stream processing jobs don’t require state: if you only need to transform one message at a time, or filter out messages based on some condition, your job can be simple. Every call to your task’s process method handles one incoming message, and each message is independent of all the other messages.

However, being able to maintain state opens up many possibilities for sophisticated stream processing jobs: joining input streams, grouping messages and aggregating groups of messages. By analogy to SQL, the select and where clauses of a query are usually stateless, but join, group by and aggregation functions like sum and count require state

#### Common use cases for stateful processing

* Windowed aggregation

Example: Counting the number of page views for each user per hour

In this case, your state typically consists of a number of counters which are incremented when a message is processed. The aggregation is typically limited to a time window (e.g. 1 minute, 1 hour, 1 day) so that you can observe changes of activity over time. This kind of windowed processing is common for ranking and relevance, detecting “trending topics”, as well as real-time reporting and monitoring.

The simplest implementation keeps this state in memory (e.g. a hash map in the task instances), and writes it to a database or output stream at the end of every time window. However, you need to consider what happens when a container fails and your in-memory state is lost. You might be able to restore it by processing all the messages in the current window again, but that might take a long time if the window covers a long period of time

Implementation: You need two processing stages.

The first one re-partitions the input data by user ID, so that all the events for a particular user are routed to the same stream task. If the input stream is already partitioned by user ID, you can skip this.
The second stage does the counting, using a key-value store that maps a user ID to the running count. For each new event, the job reads the current count for the appropriate user from the store, increments it, and writes it back. When the window is complete (e.g. at the end of an hour), the job iterates over the contents of the store and emits the aggregates to an output stream.
Note that this job effectively pauses at the hour mark to output its results. This is totally fine for Samza, as scanning over the contents of the key-value store is quite fast. The input stream is buffered while the job is doing this hourly work.


* Table-table join

Example: Join a table of user profiles to a table of user settings by user_id and emit the joined stream

If you have changelog streams for several database tables, you can write a stream processing job which keeps the latest state of each table in a local key-value store, where you can access it much faster than by making queries to the original database. Now, whenever data in one table changes, you can join it with the latest data for the same key in the other table, and output the joined result.

* Stream-table join

Example: Augment a stream of page view events with the user’s ZIP code (perhaps to allow aggregation by zip code in a later stage)

* Stream-stream join
Example: Join a stream of ad clicks to a stream of ad impressions (to link the information on when the ad was shown to the information on when it was clicked)

A stream join is useful for “nearly aligned” streams, where you expect to receive related events on several input streams, and you want to combine them into a single output event. You cannot rely on the events arriving at the stream processor at the same time, but you can set a maximum period of time over which you allow the events to be spread out.

### what is distribuetd stream processing system
Apache Samza is a distributed stream processing framework. It uses Apache Kafka for messaging, and Apache Hadoop YARN to provide fault tolerance, processor isolation, security, and resource management.

### In-memory state with checkpointing
A simple approach, common in academic stream processing systems, is to periodically save the task’s entire in-memory data to durable storage. This approach works well if the in-memory state consists of only a few values. However, you have to store the complete task state on each checkpoint, which becomes increasingly expensive as task state grows. Unfortunately, many non-trivial use cases for joins and aggregation have large amounts of state — often many gigabytes. This makes full dumps of the state impractical.

### Using an external store

Another common pattern for stateful processing is to store the state in an external database or key-value store. Conventional database replication can be used to make that database fault-tolerant. The architecture looks something like this:

![](http://samza.apache.org/img/0.7.0/learn/documentation/container/stream_job_and_db.png)

Samza allows this style of processing — there is nothing to stop you querying a remote database or service within your job. However, there are a few reasons why a remote database can be problematic for stateful stream processing:

Performance: Making database queries over a network is slow and expensive.

### Local state in Samza

Samza allows tasks to maintain state in a way that is different from the approaches described above:

* The state is stored on disk, so the job can maintain more state than would fit in memory.
* It is stored on the same machine as the processing task, to avoid the performance problems of making database queries over the network.
* Each job has its own datastore, to avoid the isolation problems of a shared database (if you make an expensive query, it affects only the current task, nobody else).
* The state is continuously replicated, enabling fault tolerance without the problems of checkpointing large amounts of state.

Imagine you take a remote database, partition it to match the number of tasks in the stream processing job, and co-locate each partition with its task. The result looks like this:

![](http://samza.apache.org/img/0.7.0/learn/documentation/container/stateful_job.png)

If a machine fails, all the tasks running on that machine and their database partitions are lost. In order to make them highly available, all writes to the database partition are replicated to a durable changelog (typically Kafka). Now, when a machine fails, we can restart the tasks on another machine, and consume this changelog in order to restore the contents of the database partition.



### unbundling

So maybe if you squint a bit, you can see the whole of your organization's systems and data flows as a single distributed database. You can view all the individual query-oriented systems (Redis, SOLR, Hive tables, and so on) as just particular indexes on your data. You can view the stream processing systems like Storm or Samza as just a very well-developed trigger and view materialization mechanism. Classical database people, I have noticed, like this view very much because it finally explains to them what on earth people are doing with all these different data systems—they are just different index types!
