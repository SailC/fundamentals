# Replication

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch05-map.png)

## Replication can serve several purposes:

1. High availability: Keeping the system running, even when one or several machines goes down
2. Latency: Placing data geographically close to the users so that users can interact with it faster
3. Scalability: handle a higher volume of reads than a single machine could, by performing reads on replicas.

## Three main approaches to replication:

1. single leader replication
    - clients send each write to a single leader node
    - leader sends a stream of data changes events to other replicas/followers.
    - reads can be performed on any replica
    - reads from the followers can be stale.

2. multi-leader replication
    - clients send each write to one of the several leader nodes
    - the leaders send streams of data changes to each other and to any follower nodes

3. leaderless replication
    - clients send each write to several nodes
    - clients read from several nodes in parallel in order to detect and correct nodes with stale data


| Pros & Cons:  | single leader | multi-leader  | leaderless |
| ------------- |:-------------:| -----:| ------:|
| simplicity     | easy  | hard | hard |
| write conflict | no conflict, dictatorship  |   yes | yes|
| consistency  | potentially linearizable |   weak | weak|
| fault tolerance  | bad     |    robust | robust|

## Replication can be synchronous & asynchronous, which has a profound effect on the system behavior when there is fault.

Asynchronous replication can be fast when the system is running smoothly. If a leader fails and you promote an asynchronously updated follower to be the new leader, recently commited data may be lost.

## How an app should behave under replication lag:

1. read-after-write consistency : user should always see data they submitted themselves

2. monotonic reads: after users have seen the data at one point in time, they shouldn't later see the data from some ealier point in time.

3. consistent prefix reads: users should see data in a state that makes causal sense, e.g. seeing a question and its reply in the correct order.

## Conflict resolution for concurrent writes
