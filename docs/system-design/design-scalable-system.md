# Design a system that scales to millions of users on AWS

## Step 1: Outline use cases and constraints

### Use cases (ask interviewer)

* **User** makes a read or write request
    * **Service** does processing, stores user data, then returns the results
* **Service** needs to evolve from serving a small amount of users to millions of users
    * Discuss general scaling patterns as we evolve an architecture to handle a large number of users and requests
* **Service** has high availability

### Constraints

* Traffic is not evenly distributed
* Need for relational data
* Scale from 1 user to tens of millions of users
    * Denote increase of users as:
        * Users+
        * Users++
        * Users+++
        * ...
    * 10 million users
    * 1 billion writes per month
    * 100 billion reads per month
    * 100:1 read to write ratio
    * 1 KB content per write

### Load parameters

* 1 TB of new content per month
    * 1 KB per write * 1 billion writes per month
    * 36 TB of new content in 3 years
    * Assume most writes are from new content instead of updates to existing ones
* 400 writes per second on average
* 40,000 reads per second on average
* [handy conversion](back-of-env/#handy-conversion-guide)

---
## Step 2: Create a high level design

> Outline a high level design with all important components.

![Imgur](http://i.imgur.com/B8LDKD7.png)

---

## Step 3: Design core components

> Dive into details for each core component.

### Use case: User makes a read or write request

#### How to design

* With only 1-2 users, you only need a basic setup
    * Single box for simplicity
    * set up monitoring stack to measure load parameters & system metrics, describe performance (percentiles) to determine bottlenecks
    * Vertical scaling when needed

#### Start with a single box
* **a virtual machine** on EC2
    * a web server handling incoming requests
    * a MySQL database running on the same machine

#### Secure the web server

* Open up only necessary ports
    * Allow the web server to respond to incoming requests from:
        * 80 for HTTP
        * 443 for HTTPS
        * 22 for SSH to only whitelisted IPs
    * Prevent the web server from initiating outbound connections

---

## Step 4: Scale the design

> Identify and address bottlenecks, given the constraints.

### Users+

![Imgur](http://i.imgur.com/rrfjMXB.png)

#### Motivation

Our user count is starting to pick up and the load is increasing on our single box.  Our **Benchmarks/Load Tests** and **Profiling** are pointing to the **MySQL Database** taking up more and more memory and CPU resources, while the user content is filling up disk space.

We've been able to address these issues with **Vertical Scaling** so far.  Unfortunately, this has become quite expensive and it doesn't allow for independent scaling of the **MySQL Database** and **Web Server**.

#### How to scale

* Lighten load on the single box and allow for independent scaling
    * Move the **MySQL Database** to a separate box
    * Simple to administer, scale
* Store static content separately in an **Object Store** (like S3)
    * Highly scalable and reliable
    * Server side encryption
    * Move static content to S3
      * User files
      * JS
      * CSS
      * Images
      * Videos
* Secure each individual box

#### Disadvantages
* These changes would increase complexity and would require changes to the **Web Server** to point to the **Object Store** and the **MySQL Database**
* Additional security measures must be taken to secure the new components
* AWS costs could also increase


### Users++

![Imgur](http://i.imgur.com/raoFTXM.png)

#### Motivation

Our **Benchmarks/Load Tests** and **Profiling** show that our single **Web Server** bottlenecks during peak hours, resulting in slow responses and in some cases, downtime.  As the service matures, we'd also like to move towards higher availability and redundancy.

#### How to scale

* Use [**Horizontal Scaling**](https://github.com/donnemartin/system-design-primer#horizontal-scaling) to handle increasing loads and to address single points of failure
    * Add a [**Load Balancer**](https://github.com/donnemartin/system-design-primer#load-balancer) such as Amazon's ELB or HAProxy
        * highly available
        * If you are configuring your own **Load Balancer**, setting up multiple servers in [active-active](https://github.com/donnemartin/system-design-primer#active-active) or [active-passive](https://github.com/donnemartin/system-design-primer#active-passive) in multiple availability zones will improve availability
        * Terminate SSL on the **Load Balancer** to reduce computational load on backend servers and to simplify certificate administration
    * Use multiple **Web Servers** spread out over multiple availability zones
    * Use multiple **MySQL** instances in [**Master-Slave Failover**](https://github.com/donnemartin/system-design-primer#master-slave-replication) mode across multiple availability zones to improve redundancy
* Separate out the **Web Servers** from the [**Application Servers**](https://github.com/donnemartin/system-design-primer#application-layer)
    * Scale and configure both layers independently
    * **Web Servers** can run as a [**Reverse Proxy**](https://github.com/donnemartin/system-design-primer#reverse-proxy-web-server)
    * For example, you can add **Application Servers** handling **Read APIs** while others handle **Write APIs**
* Move static (and some dynamic) content to a [**Content Delivery Network (CDN)**](https://github.com/donnemartin/system-design-primer#content-delivery-network) to reduce load and latency

### Users+++

![Imgur](http://i.imgur.com/OZCxJr0.png)

#### Motivation

Our **Benchmarks/Load Tests** and **Profiling** show that we are read-heavy (100:1 with writes) and our database is suffering from poor performance from the high read requests.

#### How to scale

* Move the following data to a [**Memory Cache**](https://github.com/donnemartin/system-design-primer#cache) such as Elasticache to reduce load and latency:
    * Frequently accessed content from **MySQL**
        * First, try to configure the **MySQL Database** cache to see if that is sufficient to relieve the bottleneck before implementing a **Memory Cache**
    * Session data from the **Web Servers**
        * The **Web Servers** become stateless, allowing for **Autoscaling**
    * Reading 1 MB sequentially from memory takes about 250 microseconds, while reading from SSD takes 4x and from disk takes 80x longer.<sup><a href=https://github.com/donnemartin/system-design-primer#latency-numbers-every-programmer-should-know>1</a></sup>
* Add [**MySQL Read Replicas**](https://github.com/donnemartin/system-design-primer#master-slave-replication) to reduce load on the write master
    * Add logic to **Web Server** to separate out writes and reads
    * Add **Load Balancers** in front of **MySQL Read Replicas** (not pictured to reduce clutter)
* Add more **Web Servers** and **Application Servers** to improve responsiveness

### Users++++

![Imgur](http://i.imgur.com/3X8nmdL.png)

#### Motivation

Our traffic spikes during regular business hours in the U.S. and drop significantly when users leave the office.  We think we can cut costs by automatically spinning up and down servers based on actual load.  We're a small shop so we'd like to automate as much of the DevOps as possible for **Autoscaling** and for the general operations.

#### How to Scale

* Add **Autoscaling** to provision capacity as needed
    * Keep up with traffic spikes
    * Reduce costs by powering down unused instances
* Automate DevOps
    * Chef, Puppet, Ansible, etc
* Continue monitoring metrics to address bottlenecks
    * **Host level** - Review a single EC2 instance
    * **Aggregate level** - Review load balancer stats
    * **Log analysis** - elasticsearch + logstash + kibana
    * **External site performance** - Pingdom or New Relic
    * **Handle notifications and incidents** - PagerDuty
    * **Error Reporting** - Sentry
* Disadvantages
    * Autoscaling can introduce complexity & operational surprises
    * It could take some time before a system appropriately scales up to meet increased demand, or to scale down when demand drops

### Users+++++

![Imgur](http://i.imgur.com/jj3A5N8.png)

#### Motivation
- 40k reads per second
- 400 write per second
- 1 TB of new content per month & 36 TB per year

#### How to scale

* If our **MySQL Database** starts to grow too large, we might consider only storing a limited time period of data in the database, while storing the rest in a data warehouse such as Redshift
    * A data warehouse can comfortably handle the constraint of 1 TB of new content per month

* With 40,000 average read requests per second, read traffic for popular content can be addressed by scaling the **Memory Cache**, which is also useful for handling the unevenly distributed traffic and traffic spikes

* The **SQL Read Replicas** might have trouble handling the cache misses, we'll probably need to shard/partition or federate the databases to alleviate the pressure on a single database node. In addition, 400 average writes per second (with presumably significantly higher peaks) might be tough for a single **SQL Write Master-Slave**, which also pointing to a need for additional scaling techniques

* We can further separate out our [**Application Servers**](https://github.com/donnemartin/system-design-primer#application-layer) to allow for independent scaling.  Batch processes or computations that do not need to be done in real-time can be done [**Asynchronously**](https://github.com/donnemartin/system-design-primer#asynchronism) with **Queues** and **Workers**:
    * For example, in a photo service, the photo upload and the thumbnail creation can be separated:
        * **Client** uploads photo
        * **Application Server** puts a job in a **Queue** such as SQS
        * The **Worker Service** on EC2 or Lambda pulls work off the **Queue** then:
            * Creates a thumbnail
            * Updates a **Database**
            * Stores the thumbnail in the **Object Store**
