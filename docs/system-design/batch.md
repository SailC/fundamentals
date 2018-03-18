
# Batch processing

![1](https://www.safaribooksonline.com/library/view/designing-data-intensive-applications/9781491903063/assets/ch10-map.png)

## map reduce reference

- [map reduce](http://media.jiuzhang.com/session/Chapter_6._Mapreduce2018.pdf)
- [map reduce bittiger](http://blog.bittiger.io/post164/)
- [wc](http://www.jiuzhang.com/solutions/word-count/)
- [inverted index single machine](http://www.jiuzhang.com/solution/inverted-index/)
- [inverted index map reduce](http://www.jiuzhang.com/solution/inverted-index-map-reduce/)
- [anagram single machine](http://www.jiuzhang.com/solution/anagrams/)
- [anagram map reduce](http://www.jiuzhang.com/solution/anagram-map-reduce/)
- [topk frequent](http://www.jiuzhang.com/solution/top-k-frequent-words/#tag-highlight-lang-python)
- [topk frequent map reduce](http://www.jiuzhang.com/solution/top-k-frequent-words-map-reduce/)


## external sort

* [wiki](https://zh.wikipedia.org/wiki/%E5%A4%96%E6%8E%92%E5%BA%8F)

外排序的一个例子是外归并排序（External merge sort），它读入一些能放在内存内的数据量，在内存中排序后输出为一个顺串（即是内部数据有序的临时文件），处理完所有的数据后再进行归并。比如，要对900 MB的数据进行排序，但机器上只有100 MB的可用内存时，外归并排序按如下方法操作：

1. 读入100 MB的数据至内存中，用某种常规方式（如快速排序、堆排序、归并排序等方法）在内存中完成排序。
2. 将排序完成的数据写入磁盘。
3. 重复步骤1和2直到所有的数据都存入了不同的100 MB的块（临时文件）中。在这个例子中，有900 MB数据，单个临时文件大小为100 MB，所以会产生9个临时文件。
4. 读入每个临时文件（顺串）的前10 MB（ = 100 MB / (9块 + 1)）的数据放入内存中的输入缓冲区，最后的10 MB作为输出缓冲区。（实践中，将输入缓冲适当调小，而适当增大输出缓冲区能获得更好的效果。）
执行九路归并算法，将结果输出到输出缓冲区。一旦输出缓冲区满，将缓冲区中的数据写出至目标文件，清空缓冲区。一旦9个输入缓冲区中的一个变空，就从这个缓冲区关联的文件，读入下一个10M数据，除非这个文件已读完。这是“外归并排序”能在主存外完成排序的关键步骤 -- 因为“归并算法”(merge algorithm)对每一个大块只是顺序地做一轮访问(进行归并)，每个大块不用完全载入主存。

---

## Unix tools

Some of those design principles are that inputs are immutable, outputs are intended to become the input to another (as yet unknown) program, and complex problems are solved by composing small tools that “do one thing well.”

## Two main problems

1. Partitioning
    - mappers are partitioned according to input file blocks
    - The output of mappers is repartitioned, sorted, and merged into a configurable number of reducer partitions.
    - The purpose of this process is to bring all the related data together in the same place
    - Post-MapReduce dataflow engines try to avoid sorting unless it is required

2. Fault tolerance
    - MapReduce frequently writes to disk, which makes it easy to recover from an individual failed task without restarting the entire job
    - slows down execution in the failure-free case
    - Dataflow engines perform less materialization of intermediate state and keep more in memory
    - which means that they need to recompute more data if a node fails

## Join algorithm for Mapreduce

1. sort-merge joins
    - Each of the inputs being joined goes through a mapper that extracts the join key.
    - By partitioning, sorting, and merging, all the records with the same key end up going to the same call of the reducer
    - This function can then output the joined records.

2. boardcast hash joins
    - One of the two join inputs is small, so it is not partitioned and it can be entirely loaded into a hash table.
    - you can start a mapper for each partition of the large join input, load the hash table for the small input into each mapper, and then scan over the large input one record at a time, querying the hash table for each record.

3. partitioned hash joins
    - If the two join inputs are partitioned in the same way (using the same key, same hash function, and same number of partitions), then the hash table approach can be used independently for each partition.

Distributed batch processing engines have a deliberately restricted programming model: callback functions (such as mappers and reducers) are assumed to be stateless and to have no externally visible side effects besides their designated output.

This restriction allows the framework to hide some of the hard distributed systems problems behind its abstraction: in the face of crashes and network issues, tasks can be retried safely, and the output from any failed tasks is discarded. If several tasks for a partition succeed, only one of them actually makes its output visible.

Thanks to the framework, your code in a batch processing job does not need to worry about implementing fault-tolerance mechanisms: the framework can guarantee that the final output of a job is the same as if no faults had occurred, even though in reality various tasks perhaps had to be retried. These reliable semantics are much stronger than what you usually have in online services that handle user requests and that write to databases as a side effect of processing a request.

The distinguishing feature of a batch processing job is that it reads some input data and produces some output data, without modifying the input—in other words, the output is derived from the input. Crucially, the input data is bounded: it has a known, fixed size (for example, it consists of a set of log files at some point in time, or a snapshot of a database’s contents). Because it is bounded, a job knows when it has finished reading the entire input, and so a job eventually completes when it is done.
