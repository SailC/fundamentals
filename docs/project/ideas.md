一上来就抛出各种高大上但是你根本不熟悉的关键词
• 给出一个可行方案比关键词更可靠

[container orchestration](https://medium.com/onfido-tech/container-orchestration-with-kubernetes-an-overview-da1d39ff2f91)

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
What is the right timeout before the leader is declared dead? A longer timeout means a longer time to recovery in the case where the leader fails. However, if the timeout is too short, there could be unnecessary failovers. For example, a temporary load spike could cause a node’s response time to increase above the timeout, or a network glitch could cause delayed packets. If the system is already struggling with high load or network problems, an unnecessary failover is likely to make the situation worse, not better.

---

react like SQL
In a declarative query language, like SQL or relational algebra, you just specify the pattern of the data you want—what conditions the results must meet, and how you want the data to be transformed (e.g., sorted, grouped, and aggregated)—but not how to achieve that goal. It is up to the database system’s query optimizer to decide which indexes and which join methods to use, and in which order to execute various parts of the query.


A declarative query language is attractive because it is typically more concise and easier to work with than an imperative API. But more importantly, it also hides implementation details of the database engine, which makes it possible for the database system to introduce performance improvements without requiring any changes to queries.

The SQL example doesn’t guarantee any particular ordering, and so it doesn’t mind if the order changes. But if the query is written as imperative code, the database can never be sure whether the code is relying on the ordering or not. The fact that SQL is more limited in functionality gives the database much more room for automatic optimizations.

Finally, declarative languages often lend themselves to parallel execution. Today, CPUs are getting faster by adding more cores, not by running at significantly higher clock speeds than before [31]. Imperative code is very hard to parallelize across multiple cores and multiple machines, because it specifies instructions that must be performed in a particular order. Declarative languages have a better chance of getting faster in parallel execution because they specify only the pattern of the results, not the algorithm that is used to determine the results. The database is free to use a parallel implementation of the query language, if appropriate


## mesos marathon avoid single point of failure

group configuration

brining a single point of failure down

-----

> I got to watch this data integration problem emerge in fast-forward as LinkedIn moved from a centralized relational database to a collection of distributed systems.

----
## csf architecture overview

cloud native:

netflix OSS

services provided

### goals

* Deliver open platform to host Watson cloud services that provide operational excellence
    * High availability/Auto Recovery
    * Continuous Delivery
    * Elastic to support web scale
    * Provide visibility into operations (aka Operational Visibility)
    * Security/Compliance
* Operate common services in support of Watson services
* Quickly onboard new services
* Continuously provide additional value to service teams
    * Common components
    * Tools
    * Process improvements

### netflix oss

* open sourced many of their cloud services used to run their offering, they run on AWS
* IBM took several of their OS components and ported them to Softlayer (cloud services fabric, aka CSF)
* their services to deploy image (asgard)

### What’s behind the Watson Developer Cloud
The cloud infrastructure
Running in SoftLayer
Based on CSF

### flow

datapower -> zuul (load balance) -> eureka(which server are available)

common service broker (authentication, metadata, register within bluemix)

all the authorization and authentication is provided in bluemix and handled by the datapower.

logstash -> log shipped to a centralized place -> dashboard , don't have to access to the virtual machine.

### logging
ELK stack (elastic search, logstash, kibana)

servo / statsd -> graphite -> graphana

### zuul & Eureka
zuul load balanced based on eureka info, eureka can crash, but zuul can cache the mapping with eureka client.

upgrade mesos & marathon needs that

---
## a brief introduction to mesos & marathon

why switching from vm to docker
talk about how mesos partition resources better than asgard

---

## provisioning

how to speed up the deployment process and automatically populate the attribute for agents node? -> ansible playbook , how to design an ansible playbook ? (test driven)

talk about ansible-role-base

containerize unnecessary dependencies (allow in place upgrade & decouple the app from the machine, limit the resource of the app)

---
## maintainence
mesos maintainance inverse offer

https://mesosphere.com/blog/mesos-inverse-offers/

https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Deployment%20Strategy

upgrade :
1. inplace upgrade (compatible versoin)

2. full upgrade (breaking changes)

[marathon 1.3.6 -> 1.4.2 break things](https://github.ibm.com/watson-foundation-services/tracker/issues/8215)

perform inplace upgrade is dangerous and require keeping tracking of the operations, so all the jobs needs to be run via Jenkins for record and speed.
----

## monitoring & troubleshooting

- [youtube](https://www.youtube.com/watch?v=zlgAT_xFNzU)

- health check failures
- zknode size

- [failure scenarios](https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Failure%20Scenarios)

- [sre troubleshooting tools](https://github.ibm.com/watson-foundation-services/mesos-sre-utils)

- [what to monitor](https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/W1e6642eaf1d6_456e_9c1f_1b95e4d3bbc0/page/Mesos%20Monitoring)

- [opsvis wiki](https://pages.github.ibm.com/watson-foundation-services/operational-visibility/centralized-logging/architecture/#using-logs-to-monitor-your-application)

they don't support logging from MM

```
Do we have any protips for filtering logs based on the message content? Also how much more resource intensive is this type of process

Christopher M Luciano [11:05 AM]
I want to trim the logs for Mesos basically and then only ship the important stuff to kafka
This seems to be the only way to lighten the load but I am up for other options that you can recommend

Christopher M Luciano [11:58 AM]
If I filter the log messages that I actually ship, that would help right?
my thoughts were filter at syslog level an toss to a trimmed down file, then only ship that trimmed down file

Christopher M Luciano [1:44 PM]
@tparikh: If I did the following would that be more tenable? Or are we saying the ELK stack cannot in any way support M/M logging?

Tejas Parikh [1:45 PM]
right now I cannot support it. it is not to say in future we cannot.
best approach would be that you get your own ELK
with your own dedicated kafka
if you end up hammering it with logs and bring down ELK, then only u r impacted
I cannot allow M/M logs in ELK right now
do not enable that in Softbank DEV or PROD environment @cmluciano

Christopher M Luciano [1:48 PM]
So even if I trim the logs you cannot support it?
Just trying to understand what portion is not supported. I think it’s clear that the way it is now is unsupported and that is what I am trying to fix.
My thoughts were to trim the logs to make sure that we are not sending as much data.

Tejas Parikh [1:51 PM]
there is no guarantee that your logic will control the volume.
we should get you a dedicated ELK
I cannot support M/M logs right now even with trim logic

Christopher M Luciano [1:53 PM]
Ok so should I shutdown logstash globally and remove all logstash from the ansible playbooks?

Aameek Singh [1:55 PM]
@tparikh: would that be until throttling ?

Tejas Parikh [1:56 PM]
@cmluciano: you should not configure your mesos marthong logging. DO not remove logstash. That logstash is used to ship logs from containers running
@aameek: yes until throttling is in place
```
