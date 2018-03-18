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
