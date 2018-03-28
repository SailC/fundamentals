# deep dive

## netflix oss infrastructure

I've been working as a software engineer in IBM Watson Platform team for 2 years. IBM invests a lot of money on both cloud infrastructure & Watson services, so our team is sit in the intersection of the two important businesses. The goal of the Watson platform team is to host Watson cloud services and continuously provide supports to the services team such as:

* common packages and tools required to run the services
* highly available and scalable infrastructure
* operational visibility such as monitoring & logging & metering

When I first joined the Watson Platform team, we're using several cloud service components from Netflix Open Source Software. The difference is that netflix OSS run on AWS and IBM ported them to run on Softlayer, a cloud infrastructure provider aquired by IBM.

The brief high level overview of the cloud infrastructure back then looks like:

![overview]()

1. When the traffic comes from the public internet to the private Watson cloud, it first hit the gateway, which will ask a authorization component to authorize the request.
2. After authorization, the request is passed to a loadbalancer (Zuul based), and Zuul will look up service endpoints in Eureka, which is a service discovery component that will help find the ip & port of the requested service.
3. The request is then routed to the backend services, which by then is a autoscaling group of virtual machines. The services team are provided with some base vm images that contains basic components like OS, security hardening, logging & metrics agents, and IBM Java runtime and webserver.
4. To publish a service, the services team need to build their service on top of the base images and push the images to softlayer Object store. And they can use A devops console to deploy the image into an autoscaling group. Once the vms are up & running, they will register with Eureka for future service discovery.

## moving to docker & mesos marathon

Although the autoscaling groups provides high availability & auto recovery, there are two primary reasons why we started rethink how to manage our cloud infrastructure:

1. the overhead of statically partitioning resources across vms.
2. the need to focus more on applications instead of infrastructure

We dedicate a certain number of vms to a given service, each vm has fixed amount of resources allocated to it. So as the service offering increase, it becomes more difficult to accomodate the service in the vms. e.g. when one nodejs server needs to scale up with more vms but our datacenter is aleady at its capacity limit , even now the vms of the other app sit idle, they can't give their resources to the nodejs app.  

The process of building the application on top of a base virtual machine image is actually pretty slow and complicated, we don't want the service team to spend more time on trying to get the system component working than on developing their apps.  

So the VM approach was neither efficient in terms of resource allocation nor fast or agile, so we searched for a different solution to this problem.  So we began our journey to microservices and containers, there were not so many solutions on the market as there are today. Most of them were not matured and not battle-proven. We evaluated a couple of them and finally, we decided to use Mesos and Marathon as our main framework.

With mesos, we can use the same vms in the autoscaling groups, but this time we can focus on running the applications themselves instead of virtual machine images. The applications could run on any machine with available resources. If you need to scale, you can just add vms to the mesos cluster instead of adding vms to a specific autoscaling group.

Now instead of trying to guess how many servers we need for each service and provision them into several autoscaling groups with static resources, we're able to allow the services team to dynamically request the compute, memory and storage resources they need to run.

## my role
Since we decided to transition our service runtime from auto scaling groups of virtual machines to docker container and mesos, our squad (the runtime squad) is responsible for provisioning, maintaining, monitoring & troubleshooting the mesos cluster. My work on the squad is also spreaded across those 4 areas.

### provisioning

Let's first take a look at the components that are needed to set up a mesos cluster. Our mesos cluster consists of three major components:

* mesos-masters
* mesos-slaves
* marathon (a container orchestration framework for mesos)

Mesos relies on ZooKeeper to coordinate leader election and detection within the cluster.

![](https://www.safaribooksonline.com/library/view/mesos-in-action/9781617292927/01fig07.jpg)

The machines in a cluster responsible for running the application containers are referred to as Mesos slaves. They query ZooKeeper to determine the leading Mesos master and advertise their available CPU, memory, and storage resources to the leading master in the form of a resource offer.

The mesos master is responsible for collecting resources offers from the slaves and send the offers to marathon.

Marathon is a scheduler that connects to the mesos-master and accept or reject the resource offers. Mesos delegate the responsibility of scheduling to marathon so that mesos itself can just focus on resource management and do that well. Marathon can accept or reject the resource offer, if it accept the offer, the application docker container will be launched on the mesos slave that provides the resource offer.

So a very simple set up would be just one mesos master, one mesos slave, and one marathon.

But if the mesos master is unavailable (service crash, machine offline, gc pause ...), the exisiting tasks can continue to execute, but new resources can't be allocated. To achieve high availability, we set up 5 mesos master nodes with one leader node and 4 standby node. The masters elect the leader with ZooKeeper. The same logic applies to marathon, if the single point of failure happens, new app deployment can't be scheduled and new containers can't be launched on the mesos slave nodes. So we set up 5 marathon instances on the same machine as the mesos masters.

Of course, one single slave node can't provide enough resources to run the large number of the Watson services apps, so in our environment we have hundreds of mesos-slave nodes running , each providing some amount of CPU, memory and disk (56, 256, 1T). In order to make mesos slave nodes highly available, we spread the agent across 5 availability zones and require the services team to spread their containers across the zones in order to minimize the impact when there are node failures or platform upgrades.  

Manually set up the machines one by one is obviously not possible since each mesos cluster consists of hundreds of machines. Using a shell script to provision the machine is also dangerous because the outcome can be non deterministic because each machine can have different state when the command is being executed. So we use Ansible to automate the process of configuring the system and install the needed software in the mesos cluster. We divide the machines into several groups (master , slave , marathon) and map a group of hosts to the well defined Ansible tasks. Ansible tasks is declarative and idempotent. So instead of having a shell script with imperitive command to install the software, we just need to declare the final state of the machine with ansible tasks and let ansible module handle the command execution. Re-running the playbook is much safer because the ansible module will exit without performing any actions if the final state has already been achieved.

After we start using Ansible playbook to provision the machine, we found a lot problems during the provisioning :

1. Even if most of the Ansible module claim to be indempotent, it's still tightly couple to the current state of the machine. E.g. When we're installing the same piece of software across different machines, the dependencies packages installed on one machine may be different from the other, which leads to installation failure of the package. To resolve the issue, we collect a list of the common software that's needed for the cluster (service discovery agent, logging & metrics agent) and containerize these packages to docker containers for easier start and cleaning up. Another benefit of doing this is that we can limit the amount of resources allocated to the docker container easily so that during peak time, the logging & metrics daemon won't consume huge amount of resources and impact the cluster.

2. We started running the provisioning tasks locally, but later found out it's hard to keep track of the history of the task output and who run the tasks. These information can be really valuable when troubleshooting so there needs to be centralized place logging these activities. So we later moved our provisioning tasks to Jenkins cluster and create Jenkins jobs to automate the provisioning process. Now instead of running ansible playbook locally on the laptop, we run each playbook on the Jenkins worker node, which has better network connectivity to the Softlayer machines. We can also look at the Jenkins job history to figure out who did what at which time. In addition, we can choose different environment (dev, pstg, prod) and store the environment specific configuration on a github repo so Jenkins will connect to different repo when provisioning different environment.  

3. Another issue when provisioning the machine is how to verify the mesos cluster is functioning as expected after the provisioning. So we will run some functional tests, scaling tests, and failure recovery test for newly provisioned mesos marathon cluster.  We also need to make sure the machine has all the configuration files & packages set up correctly, so we also use test infra to test the cluster setup after the provisioning. The test infra jobs are important to use because we want to make sure all the mesos clusters across different environments look identical to each other so if any upgrade compromise the dev or staging env, we can roll back the upgrade and prevent the same issue leaking to production env.

So in summary, we automate the provisioning process by leveraging Ansible, and we try to maintain consistency across the environment by dockerization the common services needed by Mesos cluster and write Jenkins pipeline that integrate the provisioning with a bunch of testing to ensure that provision leave the machine in the consistent and desirable state. Moving our devops script to Jenkins also provides a centralized logging for us to check who did what at what time when we're troubleshooting the changes that break the clusters.

### maintenance

As mesos & marathon are under active development, newer features are released, and bugs are fixed from time to time. We need to upgrade our mesos & marathon stack to the latest stable release to minimize the faults and bugs and improve the overall scalability and availability of our system.

When we're doing upgrade, it's important for us to not impact the current running services on the cluster and ensure the entire cluster stays healthy.

We break down the upgrading process to 3 major pieces, upgrading mesos-master, upgrading mesos slaves and upgrading marathon.

We need to constantly monitor the mesos & marathon logs and roll back the upgrades if anything went wrong.

the mesos cluster is able to tolerate failures caused by upgrades without impacting the overall health of the clusters.  

    * Mesos masters use a single leader and multiple standby masters, ready to take over when the leading master failed during the upgrade.

    * Checkpointing is enabled in both the marathon and on the slave, which allows the state of the cluster to be persisted periodically to disk. The checkpointed data includes information on the tasks, executors, and status updates. Slave recovery allows the mesos-slave daemon to read the state from disk and reconnect to running executors and tasks when we're upgrading the mesos-slaves.

Although features like multiple masters, check pointing and slave recovery enables Mesos & Marathon to do in-place upgrades, in reality, we sometimes simply can't achieve that due to various reasons:

1. the compatibility issues of the newer release. Newer release sometimes include breaking changes that will change the format of the cluster state information, so the slave recovery will fail
2. when we upgrade mesos cluster, we sometimes needs to perform security hardening and other kernel patches and system package, which will restart the running system services.

In either case, the running containers will be killed during the upgrade and recreated on other mesos nodes that have finished upgrading. So we have to do the upgrade carefully in a zone-by-zone fashion, because we've spread our application instances across 5 zones, having 1 node failure at a given time wouldn't cause a severe outage.

But we still need to be very careful during the upgrades, marathon and our service discovery component needs to know any action that can disrupt the cluster and cause interrupted services for the end user. Because if they are not aware of the on-going maintenance, bad things can happen.

1. even if the backend application instance is failing over to another mesos node, the the service discovery information may still be cached in the load balancer for a while before the new instance is started and turned healthy. So for the application instances that needs to be restarted during the upgrades, we need to invalidate the cache in the load balancer so that the network request won't be routed to the failed backend service instance.

2. marathon can still accept the offer from the mesos-slave node that's under maintenance and the new deployment will be launched on the maintenance nodes, which adds unnecessary burden to the cluster because the workload will be shifted to other node during the maintenance.

In order to facilitate the communication between the marathon, service discovery component and the mesos cluster that's under maintenance, we create a upgrade tool to orchestrate the process of performing upgrade of mesos slave nodes.

This tool uses the maintenance primitives provided by mesos, and the work flow of the upgrade goes like this:

1. pick a zone of slave nodes and mark those machines with `draining mode`
    * Existing resource offers will be resent from draining machines, which will contain unavailability information. Marathon will also receive inverse offerse from the mesos master to ask for resources back from marathon.
    * Now that marathon is aware of the maintenance, it will try to schedule the tasks in a way that vacate the machines before the maintenance and prevent the new tasks from being scheduled on the machines that are about to go under maintenance and reschedule the task to the healthy machines.

2. sent message to the load balancer to refresh the cache information for the service discovery component to mark the instance running on the maintenance zone as `out-of-service`. This will prevent the traffic being redirected to the unhealthy backend.

3. Once the zone has been drained, we can perform maintence on the slave zone,
    * reload the OS
    * provision new mesos slave nodes with the jenkins job (applying the kernel patches and system hardening)

4. Mark the slave nodes in the zone as `UP` so that the marathon can schedule the tasks on them again and mark the service status as `UP` so the incoming traffic can be routed to the slave nodes again.

So in summary, we try to perform the maintenance in a way that minimize the impact on the end user and the services team. Doing the upgrade manually can sometimes be time consuming and human operator can easily make mistakes when typing command and leave the cluster in a inconsistent state, and running adhoc command to performance upgrade is also hard to trace when something went wrong. So we automate the upgrading process by writing an orchestration tool to facilitate the communication among marathon, mesos and our service discovery component to minimize the noise & impact during upgrade. The automation tool not only saves our time, but it gives use much more confidence as we can test it out in dev, staging environment before put it in production, and it provides logs during the upgrade to make the communicating among the different system component much more clear and easy to trace where the error happens.

### monitoring and troubleshooting

Although we have functional test being run periodically, we still need to monitoring the metrics & logs from the mesos & marathon to ensure we can receive the alert before the outage happens.

We filter out the unhelpful logs based on our troubleshooting experience and only ship the logs that are related to the most common issues we met before. For the uncommon error and bugs, we have to ssh into the master node to check the logs line by line. We did this because mesos can go crazy generating the logs if some internal error happens, which will flood our logging backend, so we need to limit the amount and the content of the logs we are shipping.  

For mesos & marathon metrics, we also prioritize the importance and only send alerts on those critical metrics.

We focus more on the activity metrics such as

```
master leader not available
marathon leader not available
# of times for master leader election
# of times for marathon leader election
# of finished tasks
# of killed tasks
# of lost tasks
# of restarted tasks
# of health check failures
# of declined offers
```

the activity metrics usually give us a direct impression of the status of the cluster,

* when the number of healtch check failures grows, it probably indicates the marathon cluster is under heavy load or some ssl certificate is missing to perform the correct https health checks.
    * Because Marathon makes requests from a single machine — the currently leading master — it’s quite expensive, especially when you need to make thousands of HTTP requests. To reduce the load we increased the Marathon health check interval. Fortunately in the meantime Mesos incorporated HTTP health checks and they were added to Marathon 1.4, so soon we can switch and make checks locally on agents.

* when the number of declined offer increases, it probably means the resources provided by the slave nodes is not enough or the deployment has some additional constraint that can't be satisfy by the current cluster.
* when the number of times that master leader election increases, it probably means there's some problem with Zookeeper, so the quorum can't detect the current leader and view the leader offline and trigger the leader election.

We can then take one step further to look at the resources to see if the current symptom is caused by some kind of insufficient resources.

E.g. zk node size issue -> 503s

Marathon uses Zookeeper as its primary data storage. Zookeeper is a key-value store focused more on data consistency than availability. One of the disadvantages of Zookeeper is that it doesn’t work well with huge objects.

If stored objects are getting bigger, writes take more time. By default, a stored entry must fit in 1 MB

Unfortunately Marathon data layout does not fit well with this constraint. Marathon saves information about deployment statuses as old application group, deployment metadata and updated group

That means if you deploy a new application, deployment will use twice as much space as your application’s group state

when you have more and more applications, over time you will notice your Zookeeper write times take longer and at some point you will end up getting all operation blocked. Marathon 1.4.0 brings a new persistent storage layout so it might save a lot of zkNode size.

number of marathon offline > 3 -> marathon leader offline
number of master offline > 3 -> master leader offline
number of agent offline > 3 -> # of declined offer increasing
% of cpu, mem, disk -> # of declined offer


```
# zk node size
# Java Heap, normal process monitoring
# of master nodes offline
# of Marathon Process offline
# of slave nodes offline
% of cpu, mem, disk
```

We containerize the statsd and it will ping the slave node metrics point every 10 second and send the metrics to the graphite server, which we can query on Graphana.

Having the metrics and logs shipping in realtime and sending alerts help us spot the potential issue before it's causing an outage.

For newly discovered symptom on the cluster, we will document the resolution and look up the metrics and loggings to save the pattern of the metrics and logs, so we can improve our monitoring metrics based on the previous pattern.  

In summary, we're trying to minimize the outage caused by the faults of the mesos cluster. We collect the logs and metrics from mesos & marathon and ship in real-time so we can be alerted when a certain type of metrics or log pattern happens. When we're trouble shooting, we usually look at the activity metrics to get a sense of the cluster state, and then go check corresponding logs and resource metrics to identify the real cause of the issue.
