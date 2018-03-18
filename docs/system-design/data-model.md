
# Data model & query
[modeling data for document db](https://www.youtube.com/watch?v=-o_VGpJP-Q0)

[SQL vs NoSQL](http://blog.bittiger.io/post172/)

[use cases](https://github.com/FreemanZhang/system-design#nosql-vs-sql)


![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch02-map-ebook.png)

Historically, data started out being represented as big tree (the hierarchical model), but that wasn't good for representing `many-to-many relationships` , so relational model was invented to solve that problem.

More recently, developers found that some apps don't fit well in the relational model either, so non-relational `NoSQL` datastores have come into play :

1. `Document databases` target use cases where data comes in self-contained documents and relationships between one document and another are rare.

2. `Graph databases` go in the opposite direction, targeting cases where anything is potentially related to everything.

All three data models (relational, document, graph) are widely used today, each good in its respective domain. We use different data models for different purpose, not a single one-size-fits-all solution.

Non relational databases don't enforce data schema, which makes it easier for apps to adapt to changing requirements.

---

## linked-in resume example

![](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0201.png)

For a data structure like a résumé, which is mostly a self-contained document, a JSON representation can be quite appropriate

The JSON representation has better locality than the multi-table schema in Figure 2-1. If you want to fetch a profile in the relational example, you need to either perform multiple queries (query each table by user_id) or perform a messy multi-way join between the users table and its subordinate tables. In the JSON representation, all the relevant information is in one place, and one query is sufficient.

The one-to-many relationships from the user profile to the user’s positions, educational history, and contact information imply a tree structure in the data, and the JSON representation makes this tree structure explicit

![](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0202.png)

The advantage of using an ID is that because it has no meaning to humans, it never needs to change: the ID can remain the same, even if the information it identifies changes. Anything that is meaningful to humans may need to change sometime in the future—and if that information is duplicated, all the redundant copies need to be updated. That incurs write overheads, and risks inconsistencies (where some copies of the information are updated but others aren’t). Removing such duplication is the key idea behind normalization in databases.

Unfortunately, normalizing this data requires many-to-one relationships (many people live in one particular region, many people work in one particular industry), which don’t fit nicely into the document model. In relational databases, it’s normal to refer to rows in other tables by ID, because joins are easy. In document databases, joins are not needed for one-to-many tree structures, and support for joins is often weak

If the database itself does not support joins, you have to emulate a join in application code by making multiple queries to the database. (In this case, the lists of regions and industries are probably small and slow-changing enough that the application can simply keep them in memory. But nevertheless, the work of making the join is shifted from the database to the application code.)

Moreover, even if the initial version of an application fits well in a join-free document model, data has a tendency of becoming more interconnected as features are added to applications

![](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ddia_0204.png)

when it comes to representing many-to-one and many-to-many relationships, relational and document databases are not fundamentally different: in both cases, the related item is referenced by a unique identifier, which is called a `foreign key` in the relational model and a `document reference` in the document model. That identifier is resolved at read time by using a join or follow-up queries.

The main arguments in favor of the document data model are schema flexibility, better performance due to locality, and that for some applications it is closer to the data structures used by the application. The relational model counters by providing better support for joins, and many-to-one and many-to-many relationships.

However, if your application does use many-to-many relationships, the document model becomes less appealing. It’s possible to reduce the need for joins by denormalizing, but then the application code needs to do additional work to keep the denormalized data consistent. Joins can be emulated in application code by making multiple requests to the database, but that also moves complexity into the application and is usually slower than a join performed by specialized code inside the database. In such cases, using a document model can lead to significantly more complex application code and worse performance

t’s not possible to say in general which data model leads to simpler application code; it depends on the kinds of relationships that exist between data items. For highly interconnected data, the document model is awkward, the relational model is acceptable, and graph models (see “Graph-Like Data Models”) are the most natural.

---

## kv store vs. document db vs Wide column store

Key-value stores provide **high performance** and are often used for **simple data models** or for **rapidly-changing data**, such as an in-memory cache layer. Since they offer only a limited set of operations, complexity is shifted to the application layer if additional operations are needed.

A document store is centered around documents (XML, JSON, binary, etc), where a document stores all information for a given object. Document stores provide APIs or a query language to query based on the internal structure of the document itself. Note, many key-value stores include features for working with a value's metadata, blurring the lines between these two storage types.

Document stores provide **high flexibility** and are often used for working with **occasionally changing data**.

Stores such as BigTable, HBase, and Cassandra maintain keys in lexicographic order, allowing **efficient retrieval of selective key ranges**.

Wide column stores offer **high availability and high scalability**. They are often used for **very large data sets**.



## Mongo

### Storing Log Data

#### schema
The simplest approach to storing the log data would be putting the exact text of the log record into a document:

```
{
  _id: ObjectId('4f442120eb03305789000000'),
 line: '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "[http://www.example.com/start.html](http://www.example.com/start.html)" "Mozilla/4.08 [en] (Win98; I ;Nav)"'
}
```

While this solution does capture all data in a format that MongoDB can use, the data is not particularly useful, or it’s not terribly efficient: if you need to find events that the same page, you would need to use a regular expression query, which would require a full scan of the collection. The preferred approach is to extract the relevant information from the log data into individual fields in a MongoDB document.

using proper types for your data also increases query flexibility: if you store date as a timestamp you can make date range queries, whereas it’s very difficult to compare two strings that represent dates. The same issue holds for numeric fields; storing numbers as strings requires more space and is difficult to query.

```
{
     _id: ObjectId('4f442120eb03305789000000'),
     host: "127.0.0.1",
     logname: null,
     user: 'frank',
     time: ISODate("2000-10-10T20:55:36Z"),
     path: "/apache_pb.gif",
     request: "GET /apache_pb.gif HTTP/1.0",
     status: 200,
     response_size: 2326,
     referrer: "[http://www.example.com/start.html](http://www.example.com/start.html)",
     user_agent: "Mozilla/4.08 [en] (Win98; I ;Nav)"
}
```

When extracting data from logs and designing a schema, also consider what information you can omit from your log tracking system. In most cases there’s no need to track all data from an event log, and you can omit other fields. To continue the above example, here the most crucial information may be the host, time, path, user agent, and referrer, as in the following example document:

```
{
     _id: ObjectId('4f442120eb03305789000000'),
     host: "127.0.0.1",
     time:  ISODate("2000-10-10T20:55:36Z"),
     path: "/apache_pb.gif",
     referer: "[http://www.example.com/start.html](http://www.example.com/start.html)",
     user_agent: "Mozilla/4.08 [en] (Win98; I ;Nav)"
}
```

The primary performance concern for event logging systems are:

1. how many inserts per second can it support, which limits the event throughput, and

2. how will the system manage the growth of event data, particularly concerning a growth in insert activity. In most cases the best way to increase the capacity of the system is to use an architecture with some sort of partitioning or sharding that distributes writes among a cluster of systems.

#### query

* Finding All Events for a Particular Page¶

common case would be to query for all events with a specific value in the path field: This section contains a pattern for returning data and optimizing this operation.

Use a query that resembles the following to return all documents with the /apache_pb.gif value in the path field:

```
>>> q_events = db.events.find({'path': '/apache_pb.gif'})
```

Adding an index on the path field would significantly enhance the performance of this operation.

```
>>> db.events.ensure_index('path')
```

If your system has a limited amount of RAM, or your data set has a wider distribution in values, you may need to re investigate your indexing support. In most cases, however, this index is entirely sufficient.

* Finding All the Events for a Particular Date

```
>>> q_events = db.events.find('time':
...     { '$gte':datetime(2000,10,10),'$lt':datetime(2000,10,11)})
```

In this case, an index on the time field would optimize performance:

```
>>> db.events.ensure_index('time')
```

### Product Data Management¶

Product catalogs must have the capacity to store many differed types of objects with different sets of attributes.

The relational model has limited flexibility for two key reasons:

1. You must create a new table for every new category of products.
2. You must explicitly tailor all queries for the exact type of product.

Another relational data model uses a single table for all product categories and adds new columns anytime you need to store data regarding a new type of product. his approach is more flexible than concrete table inheritance: it allows single queries to span different product types, but at the expense of space.

Because MongoDB is a non-relational database, the data model for your product catalog can benefit from this additional flexibility.  The best models use a single MongoDB collection to store all the product data, which is similar to the single table inheritance relational model. MongoDB’s dynamic schema means that each document need not conform to the same schema. As a result, the document for each product only needs to contain attributes relevant to that product.

#### schema

At the beginning of the document, the schema must contain general product information, to facilitate searches of the entire catalog. Then, a details sub-document that contains fields that vary between product types. Consider the following example document for an album product.

```
{
  sku: "00e8da9b",
  type: "Audio Album",
  title: "A Love Supreme",
  description: "by John Coltrane",
  asin: "B0000A118M",

  shipping: {
    weight: 6,
    dimensions: {
      width: 10,
      height: 10,
      depth: 1
    },
  },

  pricing: {
    list: 1200,
    retail: 1100,
    savings: 100,
    pct_savings: 8
  },

  details: {
    title: "A Love Supreme [Original Recording Reissued]",
    artist: "John Coltrane",
    genre: [ "Jazz", "General" ],
        ...
    tracks: [
      "A Love Supreme Part I: Acknowledgement",
      "A Love Supreme Part II - Resolution",
      "A Love Supreme, Part III: Pursuance",
      "A Love Supreme, Part IV-Psalm"
    ],
  },
}
```

A movie item would have the same fields for general product information, shipping, and pricing, but have different details sub-document. Consider the following:

```
{
  sku: "00e8da9d",
  type: "Film",
  ...,
  asin: "B000P0J0AQ",

  shipping: { ... },

  pricing: { ... },

  details: {
    title: "The Matrix",
    director: [ "Andy Wachowski", "Larry Wachowski" ],
    writer: [ "Andy Wachowski", "Larry Wachowski" ],
    ...,
    aspect_ratio: "1.66:1"
  },
}
```

## cassandra
CQL (the Cassandra Query Language) supports defining columnfamilies with compound primary keys. The first column in a compound key definition continues to be used as the partition key, and remaining columns are automatically clustered: that is, all the rows sharing a given partition key will be sorted by the remaining components of the primary key.

```
CREATE TABLE sblocks (
    block_id uuid,
    subblock_id uuid,
    data blob,
    PRIMARY KEY (block_id, subblock_id)
)
WITH COMPACT STORAGE;
```

The first element of the primary key, block_id, is the partition key, which means that all subblocks of a given block will be routed to the same replicas. For each block, subblocks are also ordered by the subblock id

Compound keys can also be useful when denormalizing data for faster queries. Consider a Twitter data model like Twissandra's. We have tweet data:

```
CREATE TABLE tweets (
    tweet_id uuid PRIMARY KEY,
    author varchar,
    body varchar
);
```

But the most frequent query ("show me the 20 most recent tweets from people I follow") would be expensive against a normalized model. So we denormalize into another table:

```
CREATE TABLE timeline (
    user_id varchar,
    tweet_id uuid,
    author varchar,
    body varchar,
    PRIMARY KEY (user_id, tweet_id)
);
```

That is, any time a given author makes a tweet, we look up who follows him, and insert a copy of the tweet into the followers' timeline. Cassandra orders version 1 UUIDs by their time component, so

```
SELECT * FROM timeline WHERE user_id = ? ORDER BY tweet_id DESC LIMIT 20
```

requires no sort at query time.

#### under the hood

Cassandra's storage engine uses composite columns under the hood to store clustered rows. This means that all the logical rows with the same partition key get stored as a single physical "wide row." This is why Cassandra supports up to 2 billion columns per (physical) row, and why Cassandra's old Thrift api has methods to take "slices" of such rows.

To illustrate this, let's consider three tweets for our timeline data model above:

Logical representation of the denormalized timeline rows

![](https://www.datastax.com/wp-content/uploads/2012/02/Screen-shot-2012-02-16-at-4.17.44-PM.png)

Physical representation of the denormalized timeline rows
可见底层还是key value结构
![](https://www.datastax.com/wp-content/uploads/2012/02/Screen-shot-2012-02-16-at-4.20.23-PM.png)
