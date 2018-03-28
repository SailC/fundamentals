## thread vs process

![1](http://subler.github.io/note/system/img/osvm_12.jpg)

> Threads share all segments except the stack. Threads have independent call stacks, however the memory in other thread stacks is still accessible and in theory you could hold a pointer to memory in some other thread's local stack frame (though you probably should find a better place to put that memory!).


### `one thread per request` vs `event-based loop`

`one thread per request`

* overhead
    - context switch cost (CPU core limitation) (L2 cache 不停被切换）
    - Port number limitation  线程数量有上线 (TCP/IP protocol 2bytes for destination port)
    - network bottleneck for a single machine (bandwidth)
    - memory consumption
* cons:
    * don't scale well for I/O intensive workload
    * the requests spend most of the time waiting for I/O to complete
    * during this time, the resources (memory, file descriptor) linked to the worker thread is a limiting factor

* pros:
    * good for cpu intensive workload, can execute the workload simultaneously

`event based loop`

* pros:
    * the main event loop thread selects the next event to handle when I/O finished, so that thread is alwasys busy
    * good for I/O intesive workload (e.g. reserve proxy)
* cons:
    * a cpu intensive work load will suffer from the performance due to low number of concurrent process/threads

The real world senarios will be a bit in the middle, we need to balance the need for scalability with the development complexity to find the correct solution. A hybrid use case will be having an event-based front-end that delegates to the backend for the CPU intensive tasks. The front end will use little resources waiting for the task result while the back end can process multiple compute-intensive work simultaneously.

### Why node isn't exactly 'single-threaded'
It’s all a hoax. Node is multithreaded.

The main event loop is single-threaded by nature. But most of the i/o (network, disk, etc) is run on separate threads, because the i/o APIs in Node.js are asynchronous/non-blocking by design, in order to accommodate the event loop.

Let me give you an analogy. Clientside Javascript has no traditional I/O. Node.js was created in the first place because Javascript had no existing i/o libraries so they could start clean with non-blocking i/o. For the client, I/O takes the form of AJAX requests. AJAX is by default asynchronous. If AJAX were synchronous then it would lock up the front-end. By extension, the same thing is true with Node.js. If I/O in Node was synchronous/blocking then it would lock up the event-loop. Instead asynchronous/non-blocking i/o APIs in Node allow Node to utilize background threads that do the I/O work behind the scenes, thus allowing the event loop to continue ticking around and around freely, about once every 20 milliseconds.

Of course, on the backend, there are threads and processes for DB access and process execution. However, these are not explicitly exposed to your code, so you can’t worry about them other than by knowing that I/O interactions e.g. with the database, or with other processes will be asynchronous from the perspective of each request since the results from those threads are returned via the event loop to your code.

***Compared to the Apache model, there are a lot less threads and thread overhead, since threads aren’t needed for each connection; just when you absolutely positively must have something else running in parallel and even then the management is handled by Node.js.***

apache 每次客户端connection都有thread，但是这些thread不一定干活(compute or IO), 占着茅坑不拉屎的thread更多.

### nginx vs node.js

区别不是很大，一个更专业，一个更全面:

1.相似点:   

1.1异步非阻塞I/O, 事件驱动;

2.不同点:  

2.1Nginx 采用C编写，更性能更高，但是它仅适合于做web服务器，用于反向代理或者负载均衡等服务；Nginx背后的业务层编程思路很还是同步编程方式，例如PHP.  

2.2NodeJs高性能平台，web服务只是其中一块，NodeJs在处理业务层用的是JS编写,采用的是异步编程方式和思维方式。

### Apache vs nginx & node.js
* Apache
    * multithreaded
    * spawns a thread/process (depending on config) per request
    * that incurs overhead (eating memory and filedescriptor) as # of concurrent connection increases
* nginx & node.js
    * event-based asynchronous
    * threads are only needed when you absolutely positively must have something else running in parallel

## Concurrent Programming with Threads

A thread is a logical flow that runs in the context of a process.

The threads are scheduled automatically by the kernel. Each thread has its own thread context, including a unique integer thread ID (TID), stack, stack pointer, program counter, general-purpose registers, and condition codes. All threads running in a process share the entire virtual address space of that process.

A pool of concurrent threads runs in the context of a process. Each thread has its own separate thread context, which includes a thread ID, stack, stack pointer, program counter, condition codes, and general-purpose register values. Each thread shares the rest of the process context with the other threads. This includes the entire user virtual address space, which consists of read-only text (code), read/write data, the heap, and any shared library code and data areas. The threads also share the same set of open files.

Thread execution differs from processes in some important ways. Because a thread context is much smaller than a process context, a thread context switch is faster than a process context switch. Another difference is that threads, unlike pro- cesses, are not organized in a rigid parent-child hierarchy. The threads associated with a process form a pool of peers, independent of which threads were created by which other threads. The main thread is distinguished from other threads only in the sense that it is always the first thread to run in the process. The main impact of this notion of a pool of peers is that a thread can kill any of its peers, or wait for any of its peers to terminate. Further, each peer can read and write the same shared data.

In an operational sense, it is impossible for one thread to read or write the register values of another thread. On the other hand, any thread can access any location in the shared virtual memory. If some thread modifies a memory location, then every other thread will eventually see the change if it reads that location. Thus, registers are never shared, whereas virtual memory is always shared.The memory model for the separate thread stacks is not as clean. These stacks are contained in the stack area of the virtual address space, and are usually accessed independently by their respective threads. We say usually rather than always, because different thread stacks are not protected from other threads. So if a thread somehow manages to acquire a pointer to another thread’s stack, then it can read and write any part of that stack.

In general, there is no way for you to predict whether the operating system will choose a correct ordering for your threads.

---

## Using Semaphore for Mutual Exclusion

Semaphores provide a convenient way to ensure mutually exclusive access to shared variables. The basic idea is to associate a semaphore s, initially 1, with each shared variable (or related set of shared variables) and then surround the corresponding critical section with P (s) and V (s) operations.

Binary semaphores whose purpose is to provide mutual exclusion are often called mutexes. Performing a P operation on a mutex is called locking the mutex. Similarly, performing the V operation is called unlocking the mutex.

---
## Using Semaphores to Schedule Resources

Another important use of semaphores, besides providing mutual exclusion, is to schedule accesses to shared resources. In this scenario, a thread uses a semaphore operation to notify another thread that some condition in the program state has become true. Two classical and useful examples are the producer-consumer and readers-writers problems.

**Producer-consumer** interactions occur frequently in real systems. For example, in a multimedia system, the producer might encode video frames while the consumer decodes and renders them on the screen. The purpose of the buffer is to reduce jitter in the video stream caused by data-dependent differences in the encoding and decoding times for individual frames. The buffer provides a reservoir of slots to the producer and a reservoir of encoded frames to the consumer. Another common example is the design of graphical user interfaces. The producer detects mouse and keyboard events and inserts them in the buffer. The consumer removes the events from the buffer in some priority-based manner and paints the screen.

![](https://static.notion-static.com/2b0d84f8eac54241bd5648ecb75a2f72/Screen_Shot_2017-11-08_at_12.39.45_PM.png)

**Readers-writers** interactions occur frequently in real systems. For example, in an online airline reservation system, an unlimited number of customers are al- lowed to concurrently inspect the seat assignments, but a customer who is booking a seat must have exclusive access to the database. As another example, in a mul- tithreaded caching Web proxy, an unlimited number of threads can fetch existing pages from the shared page cache, but any thread that writes a new page to the cache must have exclusive access.

![](https://static.notion-static.com/adb9aeee239a4063b71a324a82bd2922/Screen_Shot_2017-11-08_at_12.45.47_PM.png)

Figure 12.26 shows a solution to the first readers-writers problem. Like the solutions to many synchronization problems, it is subtle and deceptively simple. The w semaphore controls access to the critical sections that access the shared object. The mutex semaphore protects access to the shared readcnt variable, which counts the number of readers currently in the critical section. A writer locks the w mutex each time it enters the critical section, and unlocks it each time it leaves. This guarantees that there is at most one writer in the critical section at any point in time. On the other hand, only the first reader to enter the critical section locks w, and only the last reader to leave the critical section unlocks it. The w mutex is ignored by readers who enter and leave while other readers are present. This means that as long as a single reader holds the w mutex, an unbounded number of readers can enter the critical section unimpeded.

A correct solution to either of the readers-writers problems can result in starvation, where a thread blocks indefinitely and fails to make progress. For example, in the solution in Figure 12.26, a writer could wait indefinitely while a stream of readers arrived.

## connection pool for multithreadeding performance optimizations
In the concurrent server in Figure 12.14, we created a new thread for each new client. A disadvantage of this approach is that we incur the nontrivial cost of creating a new thread for each new client. A server based on prethreading tries to reduce this overhead by using the producer-consumer model shown in Figure 12.27. The server consists of a main thread and a set of worker threads. The main thread repeatedly accepts connection requests from clients and places the resulting connected descriptors in a bounded buffer. Each worker thread repeatedly removes a descriptor from the buffer, services the client, and then waits for the next descriptor.

![](https://static.notion-static.com/decc07535ad44b2987a1717ef3b074b0/Screen_Shot_2017-11-08_at_1.03.09_PM.png)
