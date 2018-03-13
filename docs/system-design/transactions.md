## Transaction

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch07-map.png)

Transactions are an abstraction layer that allows an application to pretend that certain concurrency problems and certain kinds of hardware and software faults don’t exist. A large class of errors is reduced down to a simple transaction abort, and the application just needs to try again.

Without transactions, various error scenarios (processes crashing, network interruptions, power outages, disk full, unexpected concurrency, etc.) mean that data can become inconsistent in various ways. For example, denormalized data can easily go out of sync with the source data. Without transactions, it becomes very difficult to reason about the effects that complex interacting accesses can have on the database.

## concurrency control & isolation levels

1. read committed isolation
    - prevent dirty reads:
      One client reads another client’s writes before they have been committed.
    - prevent dirty writes:
      One client overwrites data that another client has written, but not yet committed.

2. snapshot isolation
    - prevents read skew:
      A client sees different parts of the database at different points in time.
    - some implementation of snapshot iso prevents lost updates:
      Two clients concurrently perform a read-modify-write cycle. One overwrites the other’s write without incorporating its changes, so data is lost.

3. serializable isolation
    - prevents write skew:
      A transaction reads something, makes a decision based on the value it saw, and writes the decision to the database. However, by the time the write is made, the premise of the decision is no longer true.

Weak isolation levels protect against some of those anomalies but leave you, the application developer, to handle others manually (e.g. using explicity locking). Only serializable isolation protects against all of these issues.

## implementing serializable isolation

1. Literally executing transactions in a serial order
    - make each transaction very fast to execute
    - transaction throughput is low enough to process on a single CPU core

2. Two-phase locking
    - performance sucks

3. Serializable snapshot isolation (SSI)
    - optimistic approach
    - allow transactions to proceed without blocking
    - When a transaction wants to commit, it is checked, and it is aborted if the execution was not serializable
