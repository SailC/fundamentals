总体感觉这家公司非常有朝气，办公环境还不错，包三餐。。。个人感觉如果是new gra可能需要好好准备一下behavior question。因为都给你一个情景，问你会怎么做，个人感觉好多都是我工作以后遇到的情况。不过也许new grad会问不同的问题吧。

1.vp people(完全behavior)
先给你讲他们公司的4个核心价值观，一一问你如何理解的。（大概意思，记不住原话的4个到底是什么了）1，know our customer, 问题：你会怎么满足客户的特殊需求 2，互帮互助，问题：你怎么帮助过你的同事 3.不断质疑，问题：说一件你一直觉得是对的，但是后来却发现不对的事（任何事情）4.不记得是什么了，我记得问题是 你工作以后最高兴的时候和最低潮的时候是什么 还有问题是 你觉得工作以后最大的提高是什么

2.technical
实现settimeout(function f, int delay), tick()

3.system design
caller---MessageQueue---worker---3rd party email sender

caller send request， message queue send requests to worker async, message queue 保证所有request 都被发送至少一次，request经过处理以后，把request发给第三方，第三方发送邮件给客户。存在的情况是可能一个request被重复发送，这样会重复发送邮件，现在要改变worker的设计，保证同一个request只发送一次邮件

4.technical
detect loop in directed graph，其实给你一个背景，第一要转化成图，第二要找环。还会有一些follow up，比如图有非联通的地方怎么办

5.technical
tf_idf非常straightfoward，laptop写代码

每一轮我最后都问了面试官这个问题是你的实际工作中遇到的么，因为实在不像leetcode上面的题目的感觉，他们都讲了讲实际的应用。每轮开始都会问一个关于你的project的问题，其中有一个让你在10分钟之内给他讲明白一件他完全不知道的事情(任何事情)

---


onsite从上午10点半到下午4点半结束， 有三轮coding， 一轮system design， 一轮cultral fit, 中间有跟ceo & co-founder 一起吃饭。

第一轮和第二轮是coding,算法题很简单,都是常见题型.第一轮需要在电脑上coding(最好能run). 第二轮是直接白板. 这里值得一说的是这两轮的题目都不是原题,第二轮的面试官跟我说第一轮和他这轮的题目都是从他们实际工作中遇到的问题抽象提取出来的.这点还挺有意思的.

接下来跟ceo吃饭，问了我些behaivor 问题，例如why thumbtack, what's ur passion等等, 我也问了些ceo的问题，聊的挺开心。-google 1point3acres
第三轮: vp cultralfit， vp刚从gg 跳过来三个月，之前 是gg的senior director， 我们就聊了聊我现在的proj，遇到哪些问题我怎么解决的，然后聊了聊thumbtack的tech stack他们遇到什么问题之类，这轮聊的也挺开心。

第四轮：coding， 两个面试官,一个主面一个感觉像是shallow, 比较有意思的是那个shallow的居然是HM. 主面官上来问了我很ML的问题，对我ML的proj很感兴趣, 后来居说这个面试官对ML一点不懂, 估计他就是纯粹感兴趣吧, 当然楼主我也ML的小学生,不知道他有没有懂我说的.  然后他让我写一个很简单的算法题,leetcode 中等偏下的难度. 我首先跟面试官司讨论了下题目的意思然后例了些examples,然后说了说解题的思路,面试官说思路是对的然后就让我写,写完后我解释了下我的代码,主面官说it works, 这个时候shallow的HM表示好像没怎么看懂, 我就稍微解释了下,然后他点了点头说make sense, 我当时其实并没有意识到这个shallow的原来是HM,我以为他是一个小兵,也就有些怠慢他没有进一步解释.然后就开始聊了聊他们工作的事情.

第五轮： system design, design一个跟twitter差不多的类型的app。这一轮可能是我面的最出彩的一轮，我先上最经典的3tier架构, 然后我自己不断的分析指出哪里会是瓶颈，如何优化，然后最后面试的小哥说我们thumbtack就是用这种模式，但是twitter可能会用更复杂点的架构，然后我们一起讨论，他也propose 了一些idea，我们一起探讨最后弄出了一个完整的他满意的design。
面完system design就是安排 跟hr聊天。HR很nice的送了我些纪念品文化衫，带我去天台看了看风景，然后我被送出了公司。. 鍥磋鎴戜滑@1point 3 acres

总结： thumbtack这家公司给我的感觉比较朝气蓬勃，人都很年轻，也很聪明，每个人都很nice，很有礼貌，我的所有面试中体验排第一。公司很土豪，刚融资了一个亿， office里全是27寸mac显示器。他们有一个chef在office做饭，很赞。公司ceo 很有趣，人也很nice。我个人比较喜欢thumbtack，而且比较看好他们的前景。我个人也觉得面的挺不错,有些开始期待offer了. 不过最终拿到了人生中最长的一封拒信,hr的feedback写的很详细也很真诚,大概意思是说很多人给了我strong,也有人给了no hire,他们debreif了好几次最终还是把我给拒了. 给我no hire的似乎有一个是hm,他的feedback是coding还行,但是comunication不好,所以给no hire. 我想可能是他那面我没有对他很认真的解释他没明白的地方吧.还是挺遗憾的,挺好的机会.


---

实现一个rate limiter
tree 序列化和反序列化
LFU cache
define twitter search

---

1. 给一个int流, 取值在0-1000, 求running中位数
2. Trie树, 通配符匹配
3. Design Facebook 图片相关的, 包含CDN, haystack
4. 倒排索引

---

onsite四轮技术面，一轮上
机写代码，一轮系统设计，两轮白板（如果你自告奋勇要求上机还搞定了，自然是加分
）。不难，但不刷题且非牛人还是难得过
技术面之外外有两个大佬跟你分别聊天
技术表现是主要的，但大佬们的culture fit也不能失败

---

昂赛：
第一轮是设计Todo List，算OOD吧。
第二轮是一输入一片文章，文章是map形式存储的，每个词对应的都是它在文章中出现的位置的数组。然后给你几个词，让你找在文章中包括这几个词的最短距离。
第三轮是设计一个给map encode的方法，map的key是string， value可能是list, 可能是set, 也可能是array，也可能是单个的string。

---

店面：
1. 设计数据结构，搜索prefix是否在字典中存在
2. 模糊搜索，prefix中dot表示所有可能结果

昂赛特：
1. 设计twitter的news feed，自己准备了，可怎么也没对上面试人的点
2. 设计和实现一个event calendar reminder，event有deadline
3. N个词出现在文章中的poistion (N个List），计算N的词的最短距离
3. 课程安排 （course schedule)
4／5. 和manager/VP 扯淡

---

一个年轻白人姑娘，要求写一个小游戏。本质是玩家猜个排列，三个元素，每个元素有5个可能值。猜中得奖，游戏结束。否则电脑反馈，告诉玩家某张牌错了（可能全错，但只提示一张牌）。例如：［1， 4， 3］，电脑知道正确值是［1，5，1］，所以提示第三张牌错了。

2. 系统设计。面经里有，message delivery （可能重复delivery），设计系统保证每个message 最终只deliver一次。

3. 面经题，TF_IDF ＋ top K 元素. 可以搜索wikipedia事先了解背景，免得现场学习耽误时间。

4. 设计todo list，写个class，还有 test cases。 分析／justify 数据结构的选择。

- [link](https://instant.1point3acres.com/thread/290932)

---

1. 实现一个支持timer的todo list。follow up 1：实现到时间POST到web service的功能。follow up 2：多线程怎么写

2. TF/IDF

3. 5分钟给面试官讲一个她不懂的东西 （我讲了机械工程原理。。。）
Trie实现auto complete （太累，写错了。。。）

4. Design Online Album (Flickr)

---

最近去onsite了thumbtack 估计跪了 报个面经攒人品1. 设计照片分享平台
2. TF-IDF 面经出现很多次了。本来觉得简单没有练。结果code居然没有写完。
3. 设计Todolist
用了一些multi-thread 说是coding, 不过感觉更像oo design
4. Behavior
5. 给一个query和一个doc，找minimum window snippet面经出现过
先用了类似LC 76的方法。然后被引导用inverted idx

其实都是面经题, 不过这个月onsite了5家，实在没心情把他家面经都做一遍
看面经时觉得最简单的tfidf居然跪了，其他反而答的不错

---

onsite:

1.system design

third party email sender

2. algorthm

serialize and deserialize n-ary tree

3. algorthm

if-tdf

4. algorthm

trie

补充内容 (2016-9-20 14:31):
第三题是tf-idf，写错了

补充内容 (2016-9-20 14:35):
第四题是type-ahead design + algorithm，也问了怎么存，很多怎么办，让写trie的class，和里面的function

---

面试体验来说还是不错的，题也不难，全部run过了，今天HR电话据，说是debug不好。。。
第一轮，一个拓扑排序的题
第二轮，写一个rate limiter 比LC要复杂些，和面试官确定需求
第三轮，tf-idf 之前练过了
第四轮，写一个任务管理器，两个方法insert（Pair<任务名，多少时间后执行>）, tick() 由系统调用， 如果到有到当前时间还没运行的任务，就都运行了。用java读取系统时间的函数来实现，自己设计test case模拟这个过程。
可能是最后一轮的原因，test 中tick调用时间没设计好，跑了多次才有结果。

---
