# thumbtack meeting

## meeting schedule

```
09:15AM - 09:30AM: Tracy Ng (Senior Technical Recruiter)
09:30AM - 10:00AM: Nate Kupp (Software Engineer, Team Lead)
10:00AM - 10:30AM: Raghavendra Prabhu (Engineering Director)
10:30AM - 11:00AM: Sander Daniels (Co-Founder)
11:00AM - 11:30AM: Yi Ma (Software Engineer)
11:30AM - 11:40AM: Tracy Ng (Senior Technical Recruiter)
```


Nate Kupp (Engineering Manager) - Nate may not necessarily be your manager but this is a great resource to discuss the average day of an engineer, what's expected, etc. He can also talk about working cross-functionally with other team-members and discuss internal learning/growth opportunities. Nate also came from Apple and he might be a good person to talk to about transitioning away from a gigantic corporation to a medium size company.

Questions:

- does each engineer gets assigned a single issue and work on that issue individually or pair program on a certain task ?
- how to trainsition away from a gigantic corporation to a medium size company


Rvp (Director of Engineering) - Rvp (short for Raghavendra) is one of two Eng Directors at Thumbtack. He'll most likely discuss how the Engineering team is broken out, the product roadmap + direction, eng culture, management styles, etc. He can also discuss web development and how to gain more exposure to that quickly when you join :)

Questions:

- how to grow as a web developer
- training period (what does Thumbtack expect a new commer to have ? )

Sander Daniels (Co-founder) - Sander has worked on so many important things for the company from building out our SEO strategy to currently focussing on talent hiring, diversity & inclusion, company culture. He'll talk you through Thumbtack's journey so far, company mission/goals/growth, etc.

Questions:

- story of building thumbtack (obstacles)

Questions:

Yi Ma (Software Engineer) - Yi was one of your interviews! Normally we would ask Yeming to take you to coffee or lunch but he's actually still out of office and won't return next week. Yi really enjoyed the interview with you and we thought it would a be nice for you to meet with a fellow engineer. He can give you some perspective from a peer point of view of what it's like to work at Thumbtack, our open office environment, communicating/working with other teams, etc.

Questions:

---

Thumbtack：本地服务的共享经济

成立时间：2009
上一轮估值：13亿, 1.3 billion
When I joined Thumbtack nearly three years ago, we had 25 engineers and were just beginning to scale the team (to nearly 140 engineers today!)


Thumbtack是一家提供本地服务的共享经济平台，帮助用户对接本地各种专项服务的专家。

目前提供的服务包括修水管、网络、换灯泡、修车、绘图、辅导、家政、婚纱摄影、庭院设计等700余类。

Thumbtack 通过网页端和移动应用提供普通用户和专家用户两种类型的注册。专家用户作为服务提供者需要自己提供住址，以便附近普通用户根据地理范围搜索时候能够找到自己。普通用户作为服务需求者只需选定所需服务，提供所在地，之后Thumbtack会为客户提供多名“竞价上岗”职业人员。用户通过多方对比后，进行自由选择。此外，用户还可以对职业人员进行评价，建立信誉档案。该公司在全美50个州都有业务，而且没有向美国以外的国家拓展。

Thumbtack的模式是按推介次数收费，求职成功的专业人士要向Thumbtack缴纳3到25美元的介绍费用，这确保专业人士只对他们能够完成的项目投标。

为了避免专业人士遭到虚假推介，导致他们白白付费，或是让不合格的供应商与他们竞争，Thumbtack在菲律宾建立485名员工组成的质量控制团队，负责清除垃圾邮件请求，并验证服务专业人数的资格证书。同时，Thumbtack也尝试在网站上显示平均价格数据，以便消费者能够了解到自己所在地区的这类工作大概需要付多少钱。

当硅谷的主流观念是初创企业要抓住一个垂直市场，然后深耕细作时，Thumbtack几乎同时杀进了一千个不一样的垂直市场——从修补水管到婚庆服务等等——它的目的是把各行各业的独立“手艺人”与顾客联系起来。

大多数人认为用户体验要做得简单，获取用户才会更顺利。但是Thumbtack反其道而行，在用户注册前问了一大堆超级具体的问题，都是关于他们正在寻找什么服务或者能提供什么服务的。

能成为独角兽，说明这份反常识的“耕耘”也有了属于它的那份收获，也显示Thumbtack终于占得了“本地服务O2O”这块其他公司愿意为之拼个你死我活的大蛋糕。（要知道，从Craigslist（58同城的模仿原型）的网络时代初期开始，始终没人能真正吃到这块蛋糕。）

在最终尘埃落定前，Thumbtack曾经花了不少时间低调地向各个方向都前进过。在尝试完按交易金额抽佣金和会员制收费之后，目前Thumbtack采取了向服务提供者收取单次介绍费的盈利模式。他们已经在上千个美国城市中网罗了20万服务提供者。

公司做的方向是local service的平台。这个市场非常大，目前还没有一家独大的公司，机会很好。公司的投资方有红杉资本、google capital等著名VC。

公司绿卡政策很好，new grad即使还没有拿到h1b，也会进来马上办绿卡。

```
base salary 一年工资:	170000
Equity部分(RSU/Option Total):	68175 shares (strike price 2.87, current price 8.51)
Equity Vesting schedule:	25% per year
签字费 sign on bonus:	25000
年终奖金Yearly Perf Bonus:	N/A
```

---

To me, anything that’s just operational overhead is totally orthogonal to the goals of the
business and not a worthwhile place for us to invest engineering time. In a lot of ways, we care
a lot more about that than we care about dollars. Of course, we care about minimizing our costs,
but engineering is such a scarce resource at a small startup that I think across serverless,
across managed services, that’s the compelling piece here

> Can you give an overview of the infrastructure at Thumbtack? I know your operational
infrastructure is on AWS and the data infrastructure is on Google. So you’ve got a multi-cloud
set up. Paint us a picture for how that looks.

Yeah. I like to think that anything on a synchronous path to a user is on the
AWS side, and then kind of the more offline stuff is on Google. To zoom in to each of those, so
on AWS, all of our production serving including our microservices, the remnants of the PHP
monolith, the different kind of systems supporting that, they’re all running there. We run all of our
services on Dockerized containers on ECS and we use PostgreS and Dynamo along with a little
bit of Elastic Search as our primary data stores over there. We have a bunch of touch points
where we’re kind of piping data in and out of that to the GCP side of things, primarily though
Cloud Dataproc where we run Spark jobs, and then landing an awful lot of that in BigQuery
which then feeds downstream analytics and data science and things like that.

> What’s your pipeline of
transferring data from the AWS side to the Google cloud side?

Yeah. There’s kind of two modes. We have the near real-time streaming
infrastructure and then we have batch ETL. For like our data stores for PostgreS, for Dynamo,
right now it’s mostly batch. We’re working on building change data capture out of PostgreS to
pipe that — Piping streaming changes into the Google side.
I’d say that the primary source more real-time data, we log events out of the website, out of our
services. These events are JSON or thrift objects. These hit a Fluentd cluster running on the
AWS side, which then feeds those into Google Pub/Sub and then we have various things
downstream on the Google side which subscribe to that data and process it from there.

Yeah. Basically, Kinesis the AWS version of Google Cloud Pub/Sub, so those
are pretty much one-to-one, alternative being in like Kafka if you want to self-host it. We looked
at all three. Again, I think the thing that we found really compelling about Pub/Sub and a lot of
the services in the Google side is I don’t have to worry about the knobs. Pub/Sub gives me an
API to write events and an API to subscribe and consume events and I don’t have to worry
about any of the operational details of how Google handles that on their end. Whereas like
Kinesis, I have to worry about sharding and there are some knob that are there and it’s minor,
but incrementally all these things add up and then the more kind of these knobs that we put
across our infrastructure, the more work operationally that we have to do to keep things in a
good place.

>  Okay. Cool. All these events that are coming in, the change log across the
application infrastructure goes through Fluentd, it does into Google Club Pub/Sub and then you
have several different things that are reading from that event stream. What are some of the
consumers of that event stream?

Yeah. The primary consumer today is a Spark Streaming job, which pulls
events out of these Pub/Sub topics and then writes those down into BigQuery tables. One of the
things that we’ve found pretty compelling about BigQuery was it has these streaming APIs
where I can do streaming writes into a table and it’s immediately queryable in BigQuery. That
means that like from the time a user took an action in production to the time that our analysts
can query it is like 30 seconds at scale with millions and millions of events. That’s pretty cool,
and it’s helped us a ton when we have any issues on the side and we want to understand kind
of at a higher level, kind of more of the business level rather than the engineering operations
level of what’s going on. The analyst can be a good partner to us, because they can go and look
at the events and see what’s happening.
