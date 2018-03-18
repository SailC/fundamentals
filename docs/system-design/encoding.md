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

---

## websocket

你TMD又BBB了这么久，那到底Websocket有什么鬼用，http long poll，或者ajax轮询不都可以实现实时信息传递么。

作者：Ovear
链接：https://www.zhihu.com/question/20215561/answer/40316953
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

在讲Websocket之前，我就顺带着讲下 long poll 和 ajax轮询 的原理。首先是 ajax轮询 ，ajax轮询 的原理非常简单，让浏览器隔个几秒就发送一次请求，询问服务器是否有新信息。场景再现：客户端：啦啦啦，有没有新信息(Request)服务端：没有（Response）客户端：啦啦啦，有没有新信息(Request)服务端：没有。。（Response）客户端：啦啦啦，有没有新信息(Request)服务端：你好烦啊，没有啊。。（Response）客户端：啦啦啦，有没有新消息（Request）服务端：好啦好啦，有啦给你。（Response）客户端：啦啦啦，有没有新消息（Request）服务端：。。。。。没。。。。没。。。没有（Response） ---- looplong poll long poll 其实原理跟 ajax轮询 差不多，都是采用轮询的方式，不过采取的是阻塞模型（一直打电话，没收到就不挂电话），也就是说，客户端发起连接后，如果没消息，就一直不返回Response给客户端。直到有消息才返回，返回完之后，客户端再次建立连接，周而复始。场景再现客户端：啦啦啦，有没有新信息，没有的话就等有了才返回给我吧（Request）服务端：额。。   等待到有消息的时候。。来 给你（Response）客户端：啦啦啦，有没有新信息，没有的话就等有了才返回给我吧（Request） -loop从上面可以看出其实这两种方式，都是在不断地建立HTTP连接，然后等待服务端处理，可以体现HTTP协议的另外一个特点，被动性。何为被动性呢，其实就是，服务端不能主动联系客户端，只能有客户端发起。简单地说就是，服务器是一个很懒的冰箱（这是个梗）（不会、不能主动发起连接），但是上司有命令，如果有客户来，不管多么累都要好好接待。说完这个，我们再来说一说上面的缺陷（原谅我废话这么多吧OAQ）从上面很容易看出来，不管怎么样，上面这两种都是非常消耗资源的。ajax轮询 需要服务器有很快的处理速度和资源。（速度）long poll 需要有很高的并发，也就是说同时接待客户的能力。（场地大小）所以ajax轮询 和long poll 都有可能发生这种情况。客户端：啦啦啦啦，有新信息么？服务端：月线正忙，请稍后再试（503 Server Unavailable）客户端：。。。。好吧，啦啦啦，有新信息么？服务端：月线正忙，请稍后再试（503 Server Unavailable）客户端：&lt;img src="https://pic3.zhimg.com/50/7c0cf075c7ee4cc6cf52f4572a4c1c10_hd.jpg" data-rawwidth="143" data-rawheight="50" class="content_image" width="143"&gt;然后服务端在一旁忙的要死：冰箱，我要更多的冰箱！更多。。更多。。（我错了。。这又是梗。。）--------------------------言归正传，我们来说Websocket吧通过上面这个例子，我们可以看出，这两种方式都不是最好的方式，需要很多资源。一种需要更快的速度，一种需要更多的'电话'。这两种都会导致'电话'的需求越来越高。哦对了，忘记说了HTTP还是一个无状态协议。（感谢评论区的各位指出OAQ）通俗的说就是，服务器因为每天要接待太多客户了，是个健忘鬼，你一挂电话，他就把你的东西全忘光了，把你的东西全丢掉了。你第二次还得再告诉服务器一遍。所以在这种情况下出现了，Websocket出现了。他解决了HTTP的这几个难题。首先，被动性，当服务器完成协议升级后（HTTP->Websocket），服务端就可以主动推送信息给客户端啦。所以上面的情景可以做如下修改。客户端：啦啦啦，我要建立Websocket协议，需要的服务：chat，Websocket协议版本：17（HTTP Request）服务端：ok，确认，已升级为Websocket协议（HTTP Protocols Switched）客户端：麻烦你有信息的时候推送给我噢。。服务端：ok，有的时候会告诉你的。服务端：balabalabalabala服务端：balabalabalabala服务端：哈哈哈哈哈啊哈哈哈哈服务端：笑死我了哈哈哈哈哈哈哈就变成了这样，只需要经过一次HTTP请求，就可以做到源源不断的信息传送了。（在程序设计中，这种设计叫做回调，即：你有信息了再来通知我，而不是我傻乎乎的每次跑来问你）这样的协议解决了上面同步有延迟，而且还非常消耗资源的这种情况。那么为什么他会解决服务器上消耗资源的问题呢？其实我们所用的程序是要经过两层代理的，即HTTP协议在Nginx等服务器的解析下，然后再传送给相应的Handler（PHP等）来处理。简单地说，我们有一个非常快速的接线员（Nginx），他负责把问题转交给相应的客服（Handler）。本身接线员基本上速度是足够的，但是每次都卡在客服（Handler）了，老有客服处理速度太慢。，导致客服不够。Websocket就解决了这样一个难题，建立后，可以直接跟接线员建立持久连接，有信息的时候客服想办法通知接线员，然后接线员在统一转交给客户。这样就可以解决客服处理速度过慢的问题了。同时，在传统的方式上，要不断的建立，关闭HTTP协议，由于HTTP是非状态性的，每次都要重新传输identity info（鉴别信息），来告诉服务端你是谁。虽然接线员很快速，但是每次都要听这么一堆，效率也会有所下降的，同时还得不断把这些信息转交给客服，不但浪费客服的处理时间，而且还会在网路传输中消耗过多的流量/时间。但是Websocket只需要一次HTTP握手，所以说整个通讯过程是建立在一次连接/状态中，也就避免了HTTP的非状态性，服务端会一直知道你的信息，直到你关闭请求，这样就解决了接线员要反复解析HTTP协议，还要查看identity info的信息。同时由客户主动询问，转换为服务器（推送）有信息的时候就发送（当然客户端还是等主动发送信息过来的。。），没有信息的时候就交给接线员（Nginx），不需要占用本身速度就慢的客服（Handler）了--------------------至于怎么在不支持Websocket的客户端上使用Websocket。。答案是：不能但是可以通过上面说的 long poll 和 ajax 轮询来 模拟出类似的效果
