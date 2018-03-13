![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch04-map-ebook.png)

many services need to support rolling upgrades, where a newer version of a service is gradually deployed to a few nodes at a time, rather than deploying to all nodes simutaneously.

Rolling upgrades allow newer versions of service to be released without downtime (encouraging frequent small releases over big releases) and make deployment less risky (allowing faulty releases to be detected and rolled back before they affect a large # of users). These properties are beneficial for evolvability.

During rolling upgrades, we must assume that different nodes are running different versions of our application code. Thus, it's important that all data flowing around the system is encoded in a way that provides:

- backward compatibility (new code can read old data)
- forward compatibility (old code can read new data)

Several encoding formats & their compatibility properties

1. textual formats like JSON, XML, CSV.
    - optional schema (sometimes helpful, sometimes hindrance)
    - vague about data types
    - be careful with things like numbers & binary strings

2. binary schema like Thrift, Protocol Buffer and Avro.
    - compact, efficient encoding
    - clearly defined forward & backward compatibility semantics
    - schemas useful for documentation
    - schemas useful for code generation in statically typed languages
    - data needs to be decoded before it's human readable

Several modes of data flow

1. databases.
    - process writing to the database encodes the data
    - process reading from the database decodes the data

2. RPC & REST APIs.
    - the client encodes a request
    - the server decodes the request and encodes a response
    - the client finally decodes the response

3. Asynchronous message passing.
    - using message brokers or actors
    - nodes communicate by sending each other messages that are encoded by the sender and decoded by the recipient

With a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.
