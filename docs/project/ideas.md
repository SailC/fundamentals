一上来就抛出各种高大上但是你根本不熟悉的关键词
• 给出一个可行方案比关键词更可靠

- introduction to watson platform
  * LDAP ZUUL CSB
  * neflix oss
  * eureka multi dc
  * uptime check
- marathon split to standalone
- zk issue
- provisioning (ansible)
  - ansible-role-base behavior driven
- troubleshooting
- testing
- maintainance
  - zach's automation tools (reload cluster, drain zone, upgrade cluster)
  - jenkins for automation
  - mesos in place upgrades (upgrade strategy)
- metircs & alterting (graphana, http health checks, scale test)
- mesos monitoring ? why monitor -> how to automate
  https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Monitoring
https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesosphere%20ARCA%20Questionnaire

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Profiling

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Upgrade%20Procedure

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Workflow%20-%20Docker%20Example

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Agent%20Zone%20Distribution

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Deployment%20Strategy
将 system design 的一些idea和devops的idea联系起来，希望通过之前的devops经验来apply到full stack web development上面.
从中学到了啥

how watson handle microservice


https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Docker%20Base%20images


https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Transitioning%20a%20WDC%20Service%20from%20VMs%20to%20Docker,%20Mesos,%20and%20Marathon%20(e2e%20process)

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20and%20Marathon%20Cookbook

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Failure%20Scenarios

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Eureka-Marathon%20config

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Upgrading%20a%20Mesos%20and%20Marathon%20Cluster

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/9a9d1286-4511-4353-8965-a9e157859bcb/page/c3c09b37-f4c9-447d-9b9b-b9c76360428b/attachments



https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Watson%20Platform%20Lunch%20and%20Learn

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/WDC%20ZooKeeper%20Training

https://w3-connections.ibm.com/blogs/WatsonArchitecture/entry/Migration_to_Cloud?lang=en_us

https://w3-connections.ibm.com/blogs/WatsonArchitecture/entry/Watson_Architectural_Transformation?lang=en_us

https://w3-connections.ibm.com/blogs/WatsonArchitecture/entry/Approaches_to_Moving_Faster?lang=en_us

* jenkins v.s. message que decoupling ?

---

react like SQL
In a declarative query language, like SQL or relational algebra, you just specify the pattern of the data you want—what conditions the results must meet, and how you want the data to be transformed (e.g., sorted, grouped, and aggregated)—but not how to achieve that goal. It is up to the database system’s query optimizer to decide which indexes and which join methods to use, and in which order to execute various parts of the query.


A declarative query language is attractive because it is typically more concise and easier to work with than an imperative API. But more importantly, it also hides implementation details of the database engine, which makes it possible for the database system to introduce performance improvements without requiring any changes to queries.

The SQL example doesn’t guarantee any particular ordering, and so it doesn’t mind if the order changes. But if the query is written as imperative code, the database can never be sure whether the code is relying on the ordering or not. The fact that SQL is more limited in functionality gives the database much more room for automatic optimizations.

Finally, declarative languages often lend themselves to parallel execution. Today, CPUs are getting faster by adding more cores, not by running at significantly higher clock speeds than before [31]. Imperative code is very hard to parallelize across multiple cores and multiple machines, because it specifies instructions that must be performed in a particular order. Declarative languages have a better chance of getting faster in parallel execution because they specify only the pattern of the results, not the algorithm that is used to determine the results. The database is free to use a parallel implementation of the query language, if appropriate
