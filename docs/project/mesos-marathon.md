https://allegro.tech/2017/03/hitting-the-wall.html

Running Mesosphere Marathon is like running… a marathon. When you are preparing for a long distance run, you’ll often hear about Hitting the wall. This effect is described mostly in running and cycling but affects all endurance sports. It happens when your body does not have enough glycogen to produce power and this results in a sudden “power loss” so you can’t run anymore

At Allegro we have experienced a similar thing with Mesosphere Marathon.

This is our story on using Marathon in a growing microservice ecosystem, from tens of tasks and a couple applications, to thousands of tasks and over a hundred applications.

We decided to switch to the microservice based architecture. This switch required changing our infrastructure and the way we operate and maintain our applications

We used to have one application and now we wanted to move to many small applications that could be developed, deployed, and scaled separately.

In the beginning, we tried to launch applications in dedicated VMs, but it was neither efficient in terms of resource allocation nor fast or agile, so we searched for a different solution to this problem. When we began our journey to microservices and containers, there were not so many solutions on the market as there are today. Most of them were not matured and not battle-proven. We evaluated a couple of them and finally, we decided to use Mesos and Marathon as our main framework. Below is the story of our scaling issues with Marathon as our main (and so far only) framework on top of Apache Mesos

## JVM
Marathon is written in Scala and runs on the Java Virtual Machine. Take a look at GC and heap usage metrics and if you see Marathon spends a lot of time in GC or you can’t see a saw shape on your heap utilization graph, check your GC and heap settings. There are many talks and tutorials on tuning a JVM.

## Zookeeper
Marathon uses Zookeeper as its primary data storage. Zookeeper is a key-value store focused more on data consistency than availability. One of the disadvantages of Zookeeper is that it doesn’t work well with huge objects.

If stored objects are getting bigger, writes take more time. By default, a stored entry must fit in 1 MB

Unfortunately Marathon data layout does not fit well with this constraint. Marathon saves information about deployment statuses as old application group, deployment metadata and updated group [MARATHON-1836](https://jira.mesosphere.com/browse/MARATHON-1836)

That means if you deploy a new application, deployment will use twice as much space as your application’s group state. [MARATHON-1724](https://jira.mesosphere.com/browse/MARATHON-1724)
In small installations it’s not a problem (until some of them leak MARATHON-1724), but when you have more and more applications, over time you will notice your Zookeeper write times take longer and at some point you will end up with the following error:

```javascript
422 - Failed to deploy app [/really/important/fix] to [prod].
Caused by: (http status: 422 from https://production).
RESPONSE: [{
  "message":"Object is not valid",
  "details":[{
    "path":"/",
    "errors":[
      "The way we persist data in ZooKeeper would exceed the maximum ZK node
      size (1024000 bytes). You can adjust this value via --zk_max_node_size,
      but make sure this value is compatible with your ZooKeeper ensemble!
      See: http://zookeeper.apache.org/doc/r3.3.1/zookeeperAdmin.html#Unsafe+Options"
    ]
  }]
}]
```

This was a huge problem until Marathon 0.13, but now Zookeeper compression is turned on by default. It generally works well, but still, it’s not unlimited, especially if your app definitions do not compress well

So if they don’t you will hit a wall. Marathon 1.4.0 brings [a new persistent storage layout](https://github.com/mesosphere/marathon/blob/master/changelog.md#new-zk-persistent-storage-layout) so it might save you.

Another issue with Zookeeper, like with any other high consistency storage, is the network delay between nodes. You really want to put them close to each other and to create a backup cluster in another zone/region to switch quickly in case of an outage. Having cross-DC Zookeeper clusters causes long write times and often leader reelection

Zookeeper works best if you minimize the number of objects it stores. Changing zk_max_version (deprecated) from default 25 to 5 or less will save some space. Be careful with this if you often scale your applications because you can hit MARATHON-4338 and lose your health check information.

## healthcheck

Marathon has had HTTP health checks from the beginning, before they were introduced in Mesos.Each of our tasks have a configured HTTP healthcheck. Because Marathon makes requests from a single machine — the currently leading master — it’s quite expensive, especially when you need to make thousands of HTTP requests. To reduce the load we increased the Marathon health check interval. Fortunately in the meantime Mesos incorporated HTTP health checks and they were added to Marathon 1.4, so soon we can switch and make checks locally on agents.

There is a great post on Mesos Native HTTP healtchecks. You can read there that Marathon checks work up to 2k tasks while Mesos scales well.

## sharding
If you feel like your installation could grow and want to be prepared, think about sharding. You can run many Marathon instances on a single Mesos cluster. What is more, you can run Marathon on Marathon (MoM).

---
https://github.com/spacejam/znode-size-printer
---

## problems
The way we persist data in ZooKeeper would exceed the maximum ZK node
size (1024000 bytes). You can adjust this value via --zk_max_node_size,
but make sure this value is compatible with your ZooKeeper ensemble

Marathon saves information about deployment statuses as old application group, deployment metadata and updated group

That means if you deploy a new application, deployment will use twice as much space as your application’s group state.

If you delete an application from Marathon, it also gets deleted from zookeeper. Please note, that every change to every application creates 2 new objects in zk: the version of the app and group at that point in time. There is an option to control how many versions are allowed --zk_max_versions. The default in 0.8.1 is no restriction. You should definitively set this to a reasonable size, depending how many versions you want to keep (e.g. 3). Note: setting this property will not delete anything until you change the related entity.

> what's the group:xxx data?

The stored group. group:root is the current group. group:root:TIMESTAMP is the versioned group.
You can remove all versions of the group if you like - they are there to go back in time to that version.
the same applies for app:APPNAME:TIMESTAMP.

```
13385 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp014_api-20180226-131018-7a5192.78855742-20a4-11e8-a802-e614122674e4
13387 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp010_api-20180226-131018-7a5192.78855743-20a4-11e8-a802-e614122674e4
13389 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp015_api-20180226-131018-7a5192.54e63bb1-20a4-11e8-a802-e614122674e4
13390 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp002_api-20180226-131018-7a5192.54e662c7-20a4-11e8-a802-e614122674e4
13392 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp024_api-20180226-131018-7a5192.54e662c5-20a4-11e8-a802-e614122674e4
13392 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp022_api-20180226-131018-7a5192.0f40080e-20a4-11e8-a802-e614122674e4
13394 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp001_api-20180226-131018-7a5192.3260a5ac-20a4-11e8-a802-e614122674e4
13395 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp021_api-20180226-131018-7a5192.9afb0ed7-20a4-11e8-a802-e614122674e4
13395 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp013_api-20180226-131018-7a5192.7885573c-20a4-11e8-a802-e614122674e4
13411 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp032_master-1.0.25-201803010100.7259e0e7-2160-11e8-b123-422013e1942f
13416 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp019_master-1.0.25-201803010100.c62025fa-2161-11e8-b123-422013e1942f
13418 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp008_api-20180226-131018-7a5192.9dfd0440-20a4-11e8-a802-e614122674e4
13422 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp034_master-1.0.25-201803010100.6011daf0-2160-11e8-b123-422013e1942f
13422 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp039_master-1.0.25-201803010100.1e6fa727-2164-11e8-b123-422013e1942f
13428 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp041_master-1.0.25-201803010100.53c163ac-2160-11e8-b123-422013e1942f
13428 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp039_master-1.0.25-201803010100.1e6fce38-2164-11e8-b123-422013e1942f
13428 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp037_master-1.0.25-201803010100.aa41dc23-2160-11e8-b123-422013e1942f
13431 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp019_api-20180226-131018-7a5192.54e689dd-20a4-11e8-a802-e614122674e4
13435 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp019_api-20180226-131018-7a5192.2fdb5a44-20a4-11e8-a802-e614122674e4
13438 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp018_api-20180226-131018-7a5192.78830d43-20a4-11e8-a802-e614122674e4
13439 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp005_api-20180226-131018-7a5192.9dfd0441-20a4-11e8-a802-e614122674e4
13440 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_slot-pmp005_api-20180226-131018-7a5192.78857e57-20a4-11e8-a802-e614122674e4
13451 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp010_master-1.0.25-201803010100.f08b8362-215d-11e8-b123-422013e1942f
13463 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp010_master-1.0.25-201803010100.f08bf894-215d-11e8-b123-422013e1942f
13535 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp009_master-1.0.25-201803010100.df7805ce-215d-11e8-b123-422013e1942f
13545 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp008_master-1.0.25-201803010100.1af7589d-215e-11e8-b123-422013e1942f
13568 /marathon/services_mesos_master_dal10/state/task:voyager_analytics-core-log-service_slot-pmp017_master-chi0-1.0.25-201803010100.2291082c-215f-11e8-b123-422013e1942f
14136 /marathon/services_mesos_master_dal10/state/task:dialog_dialog-ga-20171213-174544-mainstream4118-48.be7c059d-01b4-11e8-ba74-4a1971cec220
14700 /marathon/services_mesos_master_dal10/state/task:dialog_dialog-enterprise-73fa1d77-38da-4ce0-9167-8977ca4ec497-20171213-174544-mainstream4118-48.cc211af9-01b5-11e8-ba74-4a1971cec220
17748 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_api-chi1-20180226-131018-7a5192.78857e58-20a4-11e8-a802-e614122674e4
17759 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_api-chi1-20180226-131018-7a5192.9afae7bf-20a4-11e8-a802-e614122674e4
17760 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_api-chi1-20180226-131018-7a5192.61e595da-21a0-11e8-b123-422013e1942f
17763 /marathon/services_mesos_master_dal10/state/task:voyager_conversation-store_api-chi1-20180226-131018-7a5192.7885cc7f-20a4-11e8-a802-e614122674e4
469517 /marathon/services_mesos_master_dal10/state/group:root:2018-03-07T21:38:17.787Z
470308 /marathon/services_mesos_master_dal10/state/group:root:2018-03-07T20:12:44.993Z
470740 /marathon/services_mesos_master_dal10/state/group:root:2018-03-07T20:43:31.145Z
```

Marathon versions stored each group with all subgroups and applications inside a single node, which could lead to a node size larger than 1 MB, exceeding the maximum ZooKeeper node size. In version 1.4, Marathon stores a group only with references in order to keep node size under 1 MB.

The issue is that Marathon stores group defs in ZK, and the root group seems to store all the data for all child groups. When we got to a point where our /marathon/group:root znode went over about 500kb, Marathon wouldn't be able to process new deployments (we'd see either "conflicting deployment" or "futures timed out" errors in the logs). The max for any znode is 1mb, but Marathon is updating the znode with old group + deployment metadata + updated group, so the current znode doesn't even have to approach 1mb before you start seeing this problem.

Once we understood that Marathon was trying to update the group:root znode in a way that would surpass the hard limit of 1mb per znode, we were able to fiddle with our apps enough to destroy enough of them to get us below 500kb for that group:root znode. That got our dev cluster stable, but we have an upper limit on the number of app groups we can run concurrently now.

It looks like Marathon is scalable up to thousands of tasks, but those tasks need to have small definitions. We've built a "Heroku-like" system on top of Marathon for our devs, and that means that we've got a high number of apps per group, and each app has around 100 environment variables. So when your devs create multiple groups with this kind of configuration, you'll run into scalability issues sooner than you'd expect. For instance, we currently have 323 apps defined in our dev Marathon (only 120 of them actually running), but our group:root znode is over 400kb.

We're going to be rearchitecting our applications to fetch their environments themselves, instead of injecting them via the env section of the app definition. It would be good if Marathon would at least catch the exceptional case where it attempts to stuff more in the group:root znode than it can handle, and long-term to break up these potentially large znodes into parent/child znodes, or use a different data store, or something even more clever that I haven't thought of yet.

For anyone experiencing this issue: try deleting your smallest app or app group, then the next smallest, until you have control of your cluster again. That got us moving again.

---
laser is creating a huge sub group , (every time it scales down , things turns better, date back to thanks giving). be very careful about the laser group

https://ibm-watson.slack.com/archives/C2MHVQQCD/p1511423761000061
https://ibm-watson.slack.com/archives/C3NAY7FSQ/p1520302198000049

---

1. 平时工作的时候如何做贡献？
2. 怎么自动化
3. 如果有效troubleshoot
4. 如何monitor system
5. 分布式cache如何实现

---

## overview

Mesos abstracts CPU, memory, and disk resources in a way that allows datacenters to function as if they were one large machine.

Mesos creates a single underlying cluster to provide applications with the resources they need, without the overhead of virtual machines and operating systems.

just as a hypervisor abstracts physical CPU, memory, and storage resources and presents them to virtual machines, Mesos does the same but offers these resources directly to applications.

Where you once might have set up three clusters—one each to run Memcached, Jenkins CI, and your Ruby on Rails apps—you can instead deploy a single Mesos cluster to run all of these applications.

Using a combination of concepts referred to as resource offers, two-tier scheduling, and resource isolation, Mesos provides a means for the cluster to act as a single supercomputer on which to run tasks.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig02_alt.jpg)

* Resource Offers

  Mesos clusters are made up of groups of machines called masters and slaves. Each Mesos slave in a cluster advertises its available CPU, memory, and storage in the form of resource offers. As you saw in figure 1.2, these resource offers are periodically sent from the slaves to the Mesos masters, processed by a scheduling algorithm, and then offered to a framework’s scheduler running on the Mesos cluster.

* Two-tier Scheduling

In a Mesos cluster, resource scheduling is the responsibility of the Mesos master’s allocation module and the framework’s scheduler, a concept known as two-tier scheduling. As previously demonstrated, resource offers from Mesos slaves are sent to the master’s allocation module, which is then responsible for offering resources to various framework schedulers. The framework schedulers can accept or reject the resources based on their workload.

* Resource isolation

Using Linux cgroups or Docker containers to isolate processes, Mesos allows for multitenancy, or for multiple processes to be executed on a single Mesos slave. A framework then executes its tasks within the container, using a Mesos containerizer. If you’re not familiar with containers, think of them as a lightweight approach to how a hypervisor runs multiple virtual machines on a single physical host, but without the overhead or need to run an entire operating system

### Comparing virtual machines and containers

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig03_alt.jpg)

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig04_alt.jpg)

```
Service type Examples  Should you use Mesos?

Stateless—no need to persist data to disk	Web apps (Ruby on Rails, Play, Django), Memcached, Jenkins CI build slaves	Yes

Distributed out of the box	Cassandra, Elasticsearch, Hadoop Distributed File System (HDFS)	Yes, provided the correct level of redundancy is in place

Stateful—needs to persist data to disk	MySQL, PostgreSQL, Jenkins CI masters	No (version 0.22); potentially (version 0.23+)
```

The real value of Mesos is realized when running stateless services and applications—applications that will handle incoming loads but that could go offline at any time without negatively impacting the service as a whole, or services that run a job and report the result to another system.

two primary reasons that you should rethink how datacenters are managed: the administrative overhead of statically partitioning resources, and the need to focus more on applications instead of infrastructure.

Traditionally, the deployment of these services has been largely node-centric: you dedicate a certain number of machines to provide a given service. But as the infrastructure footprint expands and service offerings increase, it’s difficult to continue statically partitioning these services.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig05_alt.jpg)

Now consider solving the aforementioned scaling scenario by using Mesos, as shown in figure 1.6. You can see that you’d use these same machines in the datacenter to focus on running applications instead of virtual machines. The applications could run on any machine with available resources. If you need to scale, you add servers to the Mesos cluster, instead of adding machines to multiple clusters. If a single Mesos node goes offline, no particular impact occurs to any one service.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig06_alt.jpg)

Instead of trying to guess how many servers you need for each service and provision them into several static clusters, you’re able to allow these services to dynamically request the compute, memory, and storage resources they need to run. To continue scaling, you add new machines to your Mesos cluster, and the applications running on the cluster scale to the new infrastructure.

Operating a single, large computing cluster in this manner has several advantages:

* You can easily provision additional cluster capacity.
* You can be less concerned about where services are running.
* You can scale from several nodes to thousands.
* The loss of several servers doesn’t severely degrade any one service.

To provide services at scale, Mesos provides a distributed, fault-tolerant architecture that enables fine-grained resource scheduling. This architecture comprises three components: masters, slaves, and the applications (commonly referred to as frameworks) that run on them. Mesos relies on Apache ZooKeeper, a distributed database used specifically for coordinating leader election within the cluster, and for leader detection by other Mesos masters, slaves, and frameworks.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig07.jpg)

### masters

One or more Mesos masters are responsible for managing the Mesos slave daemons running on each machine in the cluster. Using ZooKeeper, they coordinate which node will be the leading master, and which masters will be on standby, ready to take over if the leading master goes offline.

The leading master is responsible for deciding which resources to offer to a particular framework using a pluggable allocation module, or scheduling algorithm, to distribute resource offers to the various schedulers. The scheduler can then either accept or reject the offer based on whether it has any work to be performed at that time.

A Mesos cluster requires a minimum of one master, and three or more are recommended for production deployments to ensure that the services are highly available

### slaves

The machines in a cluster responsible for executing a framework’s tasks are referred to as Mesos slaves. They query ZooKeeper to determine the leading Mesos master and advertise their available CPU, memory, and storage resources to the leading master in the form of a resource offer.

When a scheduler accepts a resource offer from the Mesos master, it then launches one or more executors on the slave, which are responsible for running the framework’s tasks.

Mesos slaves can also be configured with certain attributes and resources, which allow them to be customized for a given environment. Attributes refer to key/value pairs that might contain information about the node’s location in a datacenter, and resources allow a particular slave’s advertised CPU, memory, and disk to be overridden with user-provided values, instead of Mesos automatically detecting the available resources on the slave.

```
--attributes='datacenter:pdx1;rack:1-1;os:rhel7'
--resources='cpu:24;mem:24576;disk:409600'
```

This information is especially useful when trying to ensure that applications stay online during scheduled maintenance. Using this information, a datacenter operator could take an entire rack (or an entire row!) of machines offline for scheduled maintenance without impacting users

### frameworks

a framework is the term given to any Mesos application that’s responsible for scheduling and executing tasks on a cluster. A framework is made up of two components: a scheduler and an executor.

#### scheduler
A scheduler is typically a long-running service responsible for connecting to a Mesos master and accepting or rejecting resource offers. Mesos delegates the responsibility of scheduling to the framework, instead of attempting to schedule all the work for a cluster itself. The scheduler can then accept or reject a resource offer based on whether it has any tasks to run at the time of the offer. The scheduler detects the leading master by communicating with the ZooKeeper cluster, and then registers itself to that master accordingly.

#### executor
An executor is a process launched on a Mesos slave that runs a framework’s tasks on a slave. As of this writing, the built-in Mesos executors allow frameworks to execute shell scripts or run Docker containers. New executors can be written using Mesos’s various language bindings and bundled with the framework, to be fetched by the Mesos slave when a task requires it.

### deployments

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/03fig01_alt.jpg)

Considering that all of your cluster coordination will be happening through the Mesos masters and the ZooKeeper ensemble, you want to keep the single points of failure to a minimum. If you have multiple datacenters or a disaster recovery datacenter, you might even consider using them, assuming the network latency is low enough.

This almost goes without saying, but when deploying these services on dedicated hardware or using your virtualization or cloud provider of choice, be sure to account for redundancy at all hardware levels. If you’re running in a physical datacenter, your Mesos masters and ZooKeeper servers should perhaps be placed in different racks, connected to different (or multiple) network switches, be connected to multiple power distribution units, and so forth.

Considering that ZooKeeper is required for all coordination between Mesos masters, slaves, and frameworks, it goes without saying that it needs to be highly available for production deployments. A ZooKeeper cluster, known as an ensemble, needs to maintain a quorum, or a majority vote, within the cluster. The number of failures you’re willing to tolerate depends on your environment and service-level agreements to your users, but to create an environment that tolerates F node failures, you should deploy (2 × F + 1) machine

### HA and fault tolerant

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/04fig03_alt.jpg)

* Fault tolerance

Mesos implements two features (both enabled by default) known as checkpointing and slave recovery. Checkpointing, a feature enabled in both the framework and on the slave, allows certain information about the state of the cluster to be persisted periodically to disk. The checkpointed data includes information on the tasks, executors, and status updates.

Slave recovery allows the mesos-slave daemon to read the state from disk and reconnect to running executors and tasks should the Mesos slave daemon fail or be restarted.

* High availability

To ensure that Mesos is highly available to applications that use it as a cluster manager, the Mesos masters use a single leader and multiple standby masters, ready to take over in the event that the leading master fails. The masters use a ZooKeeper ensemble to coordinate leadership among multiple nodes, and Mesos slaves and frameworks query ZooKeeper to determine the leading master.

Through checkpointing, slave recovery, multiple masters, and coordination through ZooKeeper, the Mesos cluster is able to tolerate failures without impacting the overall health of the cluster. Because of this graceful handling of failures, Mesos is able to be upgraded without downtime as well.

----
## handling failures and upgrades

A number of events typically cause downtime and outages for infrastructure, including network partitions, machine failures, power outages, and so on

three potential failure scenarios:

* Machine failure—The underlying physical or virtual host fails.
* Service (process) failure—The mesos-master or mesos-slave daemon fails.
* Upgrades—The mesos-master or mesos-slave daemon is upgraded and restarted.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/04fig04_alt.jpg)
![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/04fig05_alt.jpg)
![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/04fig06.jpg)
![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/04fig07_alt.jpg)


## monitoring & logging
Monitoring in Mesos
In this section, we will take a look at the different metrics that Mesos provides to monitor the various components.

Monitoring provided by Mesos
Mesos master and slave nodes provide rich data that enables resource utilization monitoring and anomaly detection. The information includes details about available resources, used resources, registered frameworks, active slaves, and task state. This can be used to create automated alerts and develop a cluster health monitoring dashboard. More details can be found here:

http://mesos.apache.org/documentation/latest/monitoring/.

Network statistics for each active container are published through the /monitor/statistics.json endpoint on the slave.

TYPES OF METRICS
Mesos provides two different kinds of metrics: counters and gauges. These can be explained as follows:

Counters: This is used to measure discrete events, such as the number of finished tasks or invalid status updates. The values are always whole numbers.
Gauges: This is used to check the snapshot of a particular metric, such as the number of active frameworks or running tasks at a particular time.

Because Mesos clusters are made up of tens, hundreds, or even thousands of machines, and log files are stored on the various cluster nodes, troubleshooting issues can be a rather tedious process.

Each of these options runs a small service on each machine which then processes log files and forwards them to a centralized logging infrastructure. This allows you to store log files in a structured and searchable way, within a single data store, and easily search for and display log entries from a single console.

Although Mesos schedules resources and handles failure for you, at times you’ll need to debug failures, or access information about the cluster and its workloads. It’s helpful to know where to start debugging and what to check next. Figure 5.1 provides an example of one such troubleshooting workflow.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/05fig01_alt.jpg)

If either the mesos-master or mesos-slave services fail to start, it’s generally a good idea to start by looking in the system log for any problems. on Ubuntu, this is /var/log/syslog.

Mesos has two main services: mesos-master and mesos-slave. At the most basic level, you could configure a monitoring system to ensure that these processes are up and running on the systems that make up the Mesos cluster, but we all know that this level of monitoring usually isn’t sufficient. Fortunately, Mesos has a rich JSON-based HTTP API that you can query for more information about the health of the cluster.

### monitoring master

Monitoring the few machines that make up the Mesos master quorum is key to ensuring that your cluster continues to provide the level of service your users have come to expect, and that new tasks can be scheduled on the machines that make up the cluster. In many cases, this requires monitoring and metrics beyond basic host monitoring (CPU, memory, disk, network) and process monitoring (the mesos-master service).

Monitoring Mesos slaves is (arguably) a bit less critical than the masters because the slaves aren’t necessarily responsible for maintaining a quorum and making decisions about where to schedule tasks across the cluster. Nevertheless, the monitoring of these worker machines is as important as any other machine running in production. Without proper monitoring in place for the slaves, you run the risk of running out of resources or filling your disks without so much as a warning.

each organization and environment likely has particular thresholds for CPU, memory, and disk usage. Regardless, here are a few suggestions for monitoring checks to perform on any given Mesos slave:

Ensure that the mesos-slave process is running (and that port 5051 is accessible)
Ensure that the docker or docker.io process is running (if you’re using Docker)
Monitor basic CPU, memory, disk, and network use, ideally collected and graphed over time
Monitor per-container metrics (CPU, memory, disk, network)

---
GHE issues

[marathon stuck waiting for resources](https://github.ibm.com/watson-foundation-services/tracker/issues/9550)
[upgrade in place](https://github.ibm.com/watson-foundation-services/tracker/issues/8209)
[ghost app from marathon](https://github.ibm.com/watson-foundation-services/tracker/issues/8183)
[health check failure](https://github.ibm.com/watson-foundation-services/tracker/issues/7298)
[wiki doc](https://github.ibm.com/watson-foundation-services/runtime-documentation/wiki/Mesos-Tasks#application-configured-with-https-health-checks-failed-the-https-health-check)

[zach inplace upgrade](https://github.ibm.com/watson-foundation-services/tracker/issues/5989)


```
Currently, we are using a plugin which collects metrics information from Mesos.

Behind the scenes, it issues a call to /metrics/snapshot on the master. From there, it pulls the data and sends it to graphite.

It is based on the project located here: https://github.com/rayrod2030/collectd-mesos

```

[sre work](https://pages.github.ibm.com/watson-foundation-services/sre-watson-services/#recovery_playbooks/ldap/)

[mesos metrics](https://github.ibm.com/watson-foundation-services/tracker/issues/2955)

[graphit & syren metrics](https://github.ibm.com/watson-foundation-services/tracker/issues/4587)

[containerize dependencies](https://github.ibm.com/watson-foundation-services/tracker/issues/133)

* test
[mesos test](https://github.ibm.com/watson-foundation-services/tracker/issues/3924)

[uptime checks](https://github.ibm.com/watson-foundation-services/tracker/issues/3688)

* misc
[marathon deficiency](https://ibm.ent.box.com/notes/69072649261?s=igag8wasssr5ckun6l9ghnvfafnfhe97)



[和队友的不愉快](https://github.ibm.com/watson-foundation-services/tracker/issues/8204)
[II](https://github.ibm.com/watson-foundation-services/tracker/issues/8197)
