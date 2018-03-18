![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch01-map-alt.png)

## Reliability
Reliability means making system work correctly, even when faults occur. Fautls can be in hardware, software or human. Fault-tolerance techniques can hide certain types of faults from the end users.

## Scalability
Scalability keeps good performance even when load increases. In order to discuss scalability, we first need ways to describe load & performance quantitively.
- e.g. twitter home timeline
In a scalable system, you can add processing capacity in order to remain reliable under high load.

## Maintainability
It's about making life better for the engineering & operation teams. Good abstractions help reduce complexity & make the system easier to modify & adapt for new use cases. Good operability means having good visibility into the system's health, and having effective ways of managing it.

当我们在生产线上用一台服务器来提供数据服务的时候，我会遇到如下的两个问题：

1）一台服务器的性能不足以提供足够的能力服务于所有的网络请求。

2）我们总是害怕我们的这台服务器停机，造成服务不可用或是数据丢失。

于是我们不得不对我们的服务器进行扩展，加入更多的机器来分担性能上的问题，以及来解决单点故障问题。 通常，我们会通过两种手段来扩展我们的数据服务：

1）数据分区：就是把数据分块放在不同的服务器上（如：uid % 16，一致性哈希等）。

2）数据镜像：让所有的服务器都有相同的数据，提供相当的服务。

对于第一种情况，我们无法解决数据丢失的问题，单台服务器出问题时，会有部分数据丢失。所以，数据服务的高可用性只能通过第二种方法来完成——数据的冗余存储（一般工业界认为比较安全的备份数应该是3份，如：Hadoop和Dynamo）。 但是，加入更多的机器，会让我们的数据服务变得很复杂，尤其是跨服务器的事务处理，也就是跨服务器的数据一致性。这个是一个很难的问题。 让我们用最经典的Use Case：“A帐号向B帐号汇钱”来说明一下，熟悉RDBMS事务的都知道从帐号A到帐号B需要6个操作：

从A帐号中把余额读出来。
对A帐号做减法操作。
把结果写回A帐号中。
从B帐号中把余额读出来。
对B帐号做加法操作。
把结果写回B帐号中。
为了数据的一致性，这6件事，要么都成功做完，要么都不成功，而且这个操作的过程中，对A、B帐号的其它访问必需锁死，所谓锁死就是要排除其它的读写操作，不然会有脏数据的问题，这就是事务。那么，我们在加入了更多的机器后，这个事情会变得复杂起来：


1）在数据分区的方案中：如果A帐号和B帐号的数据不在同一台服务器上怎么办？我们需要一个跨机器的事务处理。也就是说，如果A的扣钱成功了，但B的加钱不成功，我们还要把A的操作给回滚回去。这在跨机器的情况下，就变得比较复杂了。

2）在数据镜像的方案中：A帐号和B帐号间的汇款是可以在一台机器上完成的，但是别忘了我们有多台机器存在A帐号和B帐号的副本。如果对A帐号的汇钱有两个并发操作（要汇给B和C），这两个操作发生在不同的两台服务器上怎么办？也就是说，在数据镜像中，在不同的服务器上对同一个数据的写操作怎么保证其一致性，保证数据不冲突？

同时，我们还要考虑性能的因素，如果不考虑性能的话，事务得到保证并不困难，系统慢一点就行了。除了考虑性能外，我们还要考虑可用性，也就是说，一台机器没了，数据不丢失，服务可由别的机器继续提供。 于是，我们需要重点考虑下面的这么几个情况：

1）容灾：数据不丢、结点的Failover

2）数据的一致性：事务处理

3）性能：吞吐量 、 响应时间

前面说过，要解决数据不丢，只能通过数据冗余的方法，就算是数据分区，每个区也需要进行数据冗余处理。这就是数据副本：当出现某个节点的数据丢失时可以从副本读到，数据副本是分布式系统解决数据丢失异常的唯一手段。所以，在这篇文章中，简单起见，我们只讨论在数据冗余情况下考虑数据的一致性和性能的问题。简单说来：

1）要想让数据有高可用性，就得写多份数据。

2）写多份的问题会导致数据一致性的问题。

3）数据一致性的问题又会引发性能问题

这就是软件开发，按下了葫芦起了瓢。
