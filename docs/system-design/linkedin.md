# linkedin onsite

> 设计一个logging analyzer , analyzes each exception appears how many times within given time period, how to scale

https://docs.google.com/document/d/10qRi0QJJxzH7PI_v91JCDtJb59enN2cG5T9oi7rqBfA/edit

http://massivetechinterview.blogspot.com/2016/08/system-design-interview-misc.html
https://github.com/FreemanZhang/system-design/tree/master/linkedin

https://yuelng.github.io/2015/11/13/note_system_design_question/

https://hackernoon.com/top-10-system-design-interview-questions-for-software-engineers-8561290f0444

---
system design

## TODO

* [top N exception](https://github.com/FreemanZhang/system-design/blob/master/linkedin/topk.md)
    * [my solution](./top-n-exceptions.md)
    * [map reduce](https://github.com/FreemanZhang/system-design/blob/master/topk.md)
    * service有几百个machine再跑，一段时间内top10 java exception是什么？
    * 把这些monitor service partition
    * idea solution： map reduce，用exception 的signiture来hash做reducer的key.
    * clariy & desc issue

* [trending shares](http://www.jiuzhang.com/qa/219/)
    * [my solution](./trending-shares.md)
    * top N expcetion, linkedin users不停点share， most commonly shraed articles in realtime, (not offline mapreduce)
    * [map reduce](https://github.com/FreemanZhang/system-design/blob/master/topk.md)
    * component:
        1. existing service tier that handles share events
        2. aggregation services
        3. datastore
        4. some transformation to send notificitons share event to aggregation service  
    * [design a trending topic](http://www.michael-noll.com/blog/2013/01/18/implementing-real-time-trending-topics-in-storm/)

* distributed blacklist
    * [my solution](./monitor.md)
    * [jiuzhang](https://www.jiuzhang.com/qa/6429/)
    * [jiuzhang](https://www.jiuzhang.com/qa/2651/)
    * 不怀好意的server在攻击
    * 把ip address 拉黑， ensure all webserver最新的blacklist， up to data
    * distribuetd synchronous,
    * center server -> publish blacklist -> single point, latency,
    * leaderless servers
    * use queueing system
    * number of web server
    * latency
    * datacenter  
    * bad request  
    * how to handle ddos attackers
    * server 挂了怎么办

* [hangman game](https://github.com/FreemanZhang/system-design/blob/master/linkedin/hangmanGame.md)
    * [mysolution](./hangman.md)
    * 弄一个website， allow player to player hangman， backend frontend，
    * overview diagram
    * UI
    * frontend backend api
    * interface stetches
    * details
    * friend score ranking
    * login user authentication
    * winer take money, billing & payment
    * scale
    * [jiuzhang](https://www.jiuzhang.com/qa/2655/)

* [calendering system](https://github.com/FreemanZhang/system-design/blob/master/linkedin/calendar.md)
    * [solution](https://www.jiuzhang.com/qa/3498/)
    * [jiuzhang](https://www.jiuzhang.com/qa/5490/)
    * [stackoverflow](https://stackoverflow.com/questions/12611/designing-a-calendar-system-like-google-calendar)
    * clarify requirement
    * mentioned potential issue
    * register  & create event
    * google calendar
    * write a query to determine if people are free during a certain period of time
    * how to partition data
    * website , architecture, component, db schema, SQL query

* document repository
    * [solution](./indexing-system.md)
    * [query cache](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/query_cache/README.md)
    * [design google search engine](https://softwareengineering.stackexchange.com/questions/38324/how-would-you-implement-google-search)
    * [indexing](http://www.ardendertat.com/2011/05/30/how-to-implement-a-search-engine-part-1-create-index/)
    * [another link](http://infolab.stanford.edu/~backrub/google.html)
    * [how to query](https://stackoverflow.com/questions/6032469/use-of-indexes-for-multi-word-queries-in-full-text-search-e-g-web-search)

    * a lot of docs to index, search query -> red & green & !blue ->
    * how to store the index
    * how to optimize (high freq, low freq)
    * multi-part query (先找red & green -> blue, 分层query)

* spell check
    * [hint](https://www.jiuzhang.com/qa/2263/)
    * 弄一个word processor，有spell checker，打错一个词highlight。
    * warmup 问题
    * follow up 错了之后给realtime suggestion， choose multiple suggestion ranking them, choose which one to display


* [bitly](./tinyurl.md)
    * allocate short urls
    * new url registration 100/s , redirect request 1M/s

* [autocomplete](./type-ahead.md)
    * frontend engineer
    * design an architecture for autocomplete system
    * client side component, database schema, js, css
    * make sure there is limit of chars typed
    * 打上几个字之后才发送到后端

---

manager 问法都不一样

问啥东西？

behavior question： conflict， 最骄傲的项目是那个，简要介绍一下，公司以外的项目，detail check， 希望知道平时做project的时候，接下来做什么，impact大不大，碰到问题怎么办，

更多的感受，真实地感受可以作为一个离职的原因，

也是对ibm的重要性，有很多功绩，有很多downtime， 在多少时间内把它修复的，如何修复的，后续的过程。作为一个engineer，业余的编程，我个人最喜欢的project的。

linkedin好多东西都是user facing， 很多东西都在linkedin主页上， 非常热情。 让他感觉到你做每件事情都有reason， 热情。

讲讲impact， 不要太侧重 architecture。

为什么要来linkedin？ 所以可以从对社会贡献层面上来说。 公司的mission，自己能够为linkedin带来什么？

---  

Unfortunately I don't know enough about the sorts of ways to analyze and process the data to be super helpful. But the general idea is ...
