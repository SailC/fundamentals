# Design typeahead suggestion

* [educative.io](https://www.educative.io/collection/page/5668639101419520/5649050225344512/5076324926357504)
* [interview bit](https://www.interviewbit.com/problems/design-search-typeahead/)
* [jiuzhang](http://media.jiuzhang.com/session/Crawler__Typeahead_v5.0_yBamkXj.pdf)

## Step 1: Outline use cases and constraints

### Use cases

* **User** types in their query, our service should suggest top 10 terms starting with whatever user has typed.
* **Service** has high availability
* **Service** has low latency. the suggestions should appear in real-time. The user should be able to see the suggestions within 200ms.

### Constraints

* Traffic is not evenly distributed
* Serving from cache requires fast lookups
* Low latency between machines
* Limited cache size
    * Need to determine what to keep/remove
    * Need to cache millions of queries
* 5 billion searches every day

### Load parameters
* 4 billion search / per day * 25 char per search => 100 Billion queries per day => 1 million QPS
* 15 % of the search queries are new (~500 million), 25 char per search, we have 500 Million * 25 = 12.5G perday , 50TB for 10 yrs

## Step 2: Create a high level design
![](https://dajh2p2mfq4ra.cloudfront.net/assets/site-images/system_design/typeahead_read.jpg)
![](https://dajh2p2mfq4ra.cloudfront.net/assets/site-images/system_design/typeahead_write.jpg)

## Step 3: Design core components

* Query service
	- Each time a user types a character, the entire prefix is sent to query service.
* Data collection service

### Query service DB

#### Word count table
* How to query on the db
* Query SQL: Select * from hit_stats where keyword like ${key}% order by hitCount DESC Limit 10
	- Like operation is expensive. It is a range query.
	- where keyword like 'abc%' is equivalent to where keyword >= 'abc' AND keyword < 'abd'

| keyword | hitCount |
|---------|----------|
| Amazon  | 20b      |
| Apple   | 15b      |
| Adidas  | 7b       |
| Airbnb  | 3b       |

#### Prefix table
* Convert a keyword table to a prefix table, put into memory

| prefix | keywords                     |
|--------|------------------------------|
| a      | "amazon","apple"             |
| am     | "amazon","amc"               |
| ad     | "adidas","adobe"             |
| don    | "don't have", "donald trump" |

#### Trie
* Trie ( in memory ) + Serialized Trie ( on disk ).
	- Trie is must faster than DB because
		+ All in-memory vs DB cache miss

* Store word count at node, but it's slow
	- e.g. TopK. Always need to traverse the entire trie. Exponential complexity.

* Instead, we can store the top n hot key words and their frequencies at each node, search becomes O(len).

| prefix | keywords                     |
|--------|------------------------------|
| a      | "amazon","apple"             |
| am     | "amazon","amc"               |
| ad     | "adidas","adobe"             |
| don    | "don't have", "donald trump" |

* How do we add a new record {abd: 3b} to the trie
	- Insert the record into all nodes along its path in the trie.
	- If a node along the path is already full, then need to loop through all records inside the node and compared with the node to be inserted.

* How to serialized a trie ?
    - we preorder traversal
    -  With each node we can store what character it contains and how many children it has. Right after each node we should put all of its children


### Data collections service
As the new queries come in, we can log them and also track their frequencies. Either we can log every query or do sampling and log every 1000th query. For example, if we don’t want to show a term which is searched for less than 1000 times, it’s safe to log every 1000th searched term.

We can have a Map-Reduce (MR) setup to process all the logging data periodically, say every hour. These MR jobs will calculate frequencies of all searched terms in the past hour. We can then update our trie with this new data.

* How frequently do you aggregate data
	- Real-time not impractical. Read QPS 200K + Write QPS 200K. Will slow down query service.
	- Once per week. Each week data collection service will fetch all the data within the most recent one week and aggregate them.

* How does data collection service update query service? Offline update and works online.
	- All in-memory trie must have already been serialized. Read QPS already really high. Do not write to in-memory trie directly.
	- Use another machine. Data collection service updates query service.

## Step 4: Scale the design
### How to reduce response time
* Cache result
	- Front-end browser cache the results
* Pre-fetch
	- Fetch the latest 1000 results

### What if the trie too large for one machine
* Use consistent hashing to decide which machine a particular string belongs to.
	- A record can exist only in one machine. Sharding according to char will not distribute the resource evenly. Instead, calculate consistent hashing code
	- a, am, ama, amax stored in different machines.

### How to reduce the size of log file
* Probablistic logging.
	- Too slow to calculate and too large amount of data to store.
	- Log with 1/10,000 probability
		+ Say over the past two weeks "amazon" was searched 1 billion times, with 1/1000 probability we will only log 1 million times.
		+ For a term that's searched 1000 times, we might end up logging only once or even zero times.
