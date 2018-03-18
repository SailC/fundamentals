# Consistency & Consensus

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch09-map-ebook.png)

## Linearizability

its goal is to make replicated data appear as though there were only a single copy, and to make all operations act on it atomically.

Although linearizability is appealing because it is easy to understand—it makes a database behave like a variable in a single-threaded program—it has the downside of being slow, especially in environments with large network delays.

## Causality
it imposes an ordering on events in a system (what happened before what, based on cause and effect).

Unlike linearizability, which puts all operations in a single, totally ordered timeline, causality provides us with a weaker consistency model: some things can be concurrent, so the version history is like a timeline with branching and merging.

Causal consistency does not have the coordination overhead of linearizability and is much less sensitive to network problems.

However, even if we capture the causal ordering (for example using Lamport timestamps), we saw that some things cannot be implemented this way.

we considered the example of ensuring that a username is unique and rejecting concurrent registrations for the same username. If one node is going to accept a registration, it needs to somehow know that another node isn’t concurrently in the process of registering the same name. This problem led us toward consensus.

## Consensus
consensus means deciding something in such a way that all nodes agree on what was decided, and such that the decision is irrevocable.

Such equivalent problems include:

1. Linearizable compare-and-set registers
2. Atomic transaction commit
3. Total order broadcast
4. Locks and leases
5. Membership/coordination service
6. Uniqueness constraint

All of these are straightforward if you only have a single node, or if you are willing to assign the decision-making capability to a single node. This is what happens in a single-leader database: all the power to make decisions is vested in the leader, which is why such databases are able to provide linearizable operations, uniqueness constraints, a totally ordered replication log, and more

However, if that single leader fails, or if a network interruption makes the leader unreachable, such a system becomes unable to make any progress.
There are three ways of handling that situation:

1. Wait for the leader to recover, and accept that the system will be blocked in the meantime.
2. Manually fail over by getting humans to choose a new leader node and reconfigure the system to use it.
3. Use an algorithm to automatically choose a new leader.

Although a single-leader database can provide linearizability without executing a consensus algorithm on every write, it still requires consensus to maintain its leadership and for leadership changes. Thus, in some sense, having a leader only “kicks the can down the road”: consensus is still required, only in a different place, and less frequently.

Nevertheless, not every system necessarily requires consensus: for example, leaderless and multi-leader replication systems typically do not use global consensus. The conflicts that occur in these systems (see “Handling Write Conflicts”) are a consequence of not having consensus across different leaders, but maybe that’s okay: maybe we simply need to cope without linearizability and learn to work better with data that has branching and merging version histories
