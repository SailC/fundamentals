[bellman-ford](https://www.youtube.com/watch?v=9PHkk0UavIM)
## [course schedule](https://leetcode.com/problems/course-schedule/description/)

`有思路` `回味` `topological sort` `dfs/bfs`

> 这题的本质是检测有向图有没有环，如果有环，那么环内部的节点不存在入度为0的情况，就不可能找到拓扑排序。
> 1. topological sorting 如果有环，遍历所得到的节点不可能为所有节点
> 2. dfs，随便找一个节点开始dfs，如果下一个节点已经visited过，说明有环。如果遍历完所有节点之后还没有找到环，就说明没有环, DAG图是肯定拓扑有序滴！A topological ordering is possible if and only if the graph has no directed cycles, that is, if it is a directed acyclic graph (DAG). Any DAG has at least one topological ordering, and algorithms are known for constructing a topological ordering of any DAG in linear time.
dfs的时候为了避免从原来已经遍历过的节点重新出发，用一个全局的visited set来记录已经作为起点处罚过的节点。Time complexity = O(V + E). V is # of vertices, E is # of edges

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/207-ep93.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/207-ep93-1.png)

```javascript
var canFinish = function(numCourses, prerequisites) {
    let indegree = new Array(numCourses).fill(0);
    let outs = new Array(numCourses).fill(0).map(x => []);
    for (let [to, from] of prerequisites) {
        indegree[to]++;
        outs[from].push(to);
    }
    // bfs
    let que = [], cnt = 0;
    for (let i = 0; i < numCourses; i++) {
        if (indegree[i] === 0) que.push(i);
    }
    while (que.length > 0) {
        let course = que.shift();
        cnt++;
        for (let to of outs[course]) {
            if (--indegree[to] === 0) que.push(to);
        }
    }
    return cnt === numCourses ? true : false;
};

canFinish = function(numCourses, prerequisites) {
    let n = numCourses;
    let graph = new Array(n).fill(0).map(x => []);
    for (let [dest, src] of prerequisites) graph[src].push(dest);

    const UNVISITED = 0, VISITING = 1, VISITED = 2;
    let status = new Array(n).fill(UNVISITED);

    function hasCycle(i) {
        if (status[i] === VISITING) return true;
        status[i] = VISITING;
        for (let adj of graph[i]) {
            if (hasCycle(adj)) return true;
        }
        status[i] = VISITED;
        return false;
    }

    for (let i = 0; i < n; i++) {
        if (status[i] === UNVISITED && hasCycle(i)) return false;
    }

    return true;
};
```

---

## [course schedule II](https://leetcode.com/problems/course-schedule-ii/description/)

`有思路` `回味` `topological sort` `dfs/bfs`

> You may assume that there are no duplicate edges in the input prerequisites -> indegree can use course -> cnt (if dup, cnt will not be correct, has to use set)

1. bfs
> topological sort bfs doesn't have to worry about the loop in the cycle, because if there is a cycle , the nodes within the cycle won't have indegree of 1 so they'll never be added into the que -> which means the traversal won't cover all the nodes in the graph
> We observe that if a node has incoming edges, it has prerequisites. Therefore, the first few in the order must be those with no prerequisites

> Time: O(V + E) ~ O(V ^ 2)
> space: O(V + E) ~ O(V ^ 2)

2. dfs
> 如果检测出环，则没有topology
> 如果没有检测出环，则按照后序遍历存储visited的 node，最后将他们reverse。后续遍历的好处是确保这个node所有的children都visit过, 没有后顾之忧。preorder的话你不清楚child node的情况，不敢贸然决定sorted的order
> 拓扑排序之后的最后几个node必定不是作为别人prereq的course，否则，他们的后续课程一定比他们排序的后. 所以我们在退栈的时候将node mark一下成visited。

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/210-ep133.png)

```javascript
var findOrder = function(numCourses, prerequisites) {
    let [ind, outs] = parse(numCourses, prerequisites);
    let que = [];
    for (let i = 0; i < numCourses; i++) {
        if (ind[i] === 0) que.push(i);
    }
    let order = [];
    while (que.length > 0) {
        let course = que.shift();
        order.push(course);
        for (let nextCourse of outs[course]) {
            if (--ind[nextCourse] === 0) que.push(nextCourse);
        }
    }
    return order.length === numCourses ? order : [];
};

findOrder = function(numCourses, prerequisites) {
    let [_, graph] = parse(numCourses, prerequisites);
    const UNVISITED = 0, VISITING = 1, VISITED = 2;
    let status = new Array(numCourses).fill(UNVISITED);
    let order = [];

    function dfs(course) {
        if (status[course] === VISITING) return true;// cycle detection
        if (status[course] === VISITED) return false;
        status[course] = VISITING;
        for (let neighbor of graph[course]) {
            if (dfs(neighbor)) return true;
        }
        status[course] = VISITED;
        order.push(course); // post order dfs.
        return false;
    }

    for (let i = 0; i < numCourses; i++) {
        if (dfs(i)) return [];
    }

    return order.reverse();
};


function parse(n, pre) {
    let ind = new Array(n).fill(0);
    let outs = new Array(n).fill(0).map(x => []);
    for (let [to, from] of pre) {
        ind[to]++;
        outs[from].push(to);
    }
    return [ind, outs];
}
```

---
## [closest leaf in a binary tree](https://leetcode.com/problems/closest-leaf-in-a-binary-tree/description/)

`无思路` `outofbox` `shortest path`

1. dfs + bfs
> 用dfs建图, bfs 找到最短路径
> graph 每个节点最多只有三个neighbors，所以时间复杂度和空间复杂度都是线性
> bfs 可以从target出发找leaves，也可以从leaves出发找target

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/742-ep131.png)

```javascript
var findClosestLeaf = function(root, k) {
    let graph = new Map();
    let leaves = [], target = null;
    function dfs(node, parent) {
        if (!node) return;
        if (node.val === k) target = node;
        if (!node.left && !node.right) leaves.push(node);
        if (!graph.has(node)) graph.set(node, []);
        let neighbors = graph.get(node);
        if (parent) neighbors.push(parent);
        if (node.left) neighbors.push(node.left);
        if (node.right) neighbors.push(node.right);
        dfs(node.left, node);
        dfs(node.right, node);
    }
    dfs(root, null);
    //graph is constructed
    // bfs
    let que = leaves.map(x => [x, x.val]);
    let visited = new Set(leaves);
    while (que.length > 0) {
        let [node, mark] = que.shift();
        if (node === target) return mark;
        for (let neighbor of graph.get(node)) {
            if (visited.has(neighbor)) continue;
            visited.add(neighbor);
            que.push([neighbor, mark]);
        }
    }
};
```
---
## [Network Delay time](https://leetcode.com/problems/network-delay-time/description/)
`无思路` `套路` `单源最短路径`

> 单源最短路径
1. dfs
> 从k node 出发，如果有多条路线到达dest node的话，用到达时的time来判重避免无限循环，只有time小于的时候说明找到一条更短的路径，可以继续dfs下去.
> Time: O(V^V) 对于每个节点，都可能由 V - 1 个neighbor到达，而对每个neighbor，有可能由 V - 1个neighbor到达.
> Space: O(V + E), the size of graph O(E) + the size of the stack O(V)
2. bellman-ford

```javascript
var networkDelayTime = function(times, N, K) {
    let graph = new Array(N).fill(0).map(x => []);
    for (let [u, v, w] of times) graph[u - 1].push([v - 1, w]);
    let dist = new Array(N).fill(Infinity);
    // dist[K - 1] = 0; bug

    function dfs(node, time) {
        if (time >= dist[node]) return;
        dist[node] = time;
        for (let [neighbor, t] of graph[node]) {
            dfs(neighbor, time + t);
        }
    }

    dfs(K - 1, 0);
    let maxTime = Math.max(...dist);
    return maxTime === Infinity ? -1 : maxTime;
};

networkDelayTime = function(times, N, K) {
    let dist = new Array(N).fill(Infinity);
    dist[K - 1] = 0;
    for (let i = 0; i < N; i++) {
        for (let [u, v, w] of times) {
            dist[v - 1] = Math.min(dist[v - 1], dist[u - 1] + w);
        }
    }
    let maxTime = Math.max(...dist);
    return maxTime === Infinity ? -1 : maxTime;
};

networkDelayTime = function(times, N, K) {
    let dist = new Array(N).fill(0).map(x => new Array(N).fill(Infinity));
    for (let [u, v, w] of times) dist[u - 1][v - 1] = w;
    for (let i = 0; i < N; i++) dist[i][i] = 0;

    for (let k = 0; k < N; k++) {
        for (let i = 0; i < N; i++) {
            for (let j = 0; j < N; j++) {
                dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
            }
        }
    }

    let maxTime = Math.max(...dist[K - 1]);
    return maxTime === Infinity ? -1 : maxTime;
};
```
---
## [cheapest flights within k stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/description/)

`无思路` `套路` `单源最短路径`

1. dfs
> 从src出发，dfs更新到达各个node的最短路径。用visited数组避免cycle。注意prune，当hop到达一定个数，以及cost到达minCost的时候。
> Time: O(N ^ K), 最多走K步, 每一步有N个adj
> Space: O(K)
2. bfs
> 每个que的节点保存到该node目前的最短路径。注意保存hop信息和cost信息，prune的code位置也不一样。
> Time: O(N ^ K)
> Space: O(N ^ K)
3. bellman ford
> 外循环k + 1次，每次扫一遍所有的边(u, v, w)，尝试更新到达v， 步数为 i + 1 的最短路径.
> Time: O(N * K)
> Space: O(N * K) -> O(N)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/02/787-ep170.png)

```javascript
var findCheapestPrice = function(n, flights, src, dst, K) {
    let cost = new Array(n).fill(Infinity);
    cost[src] = 0;
    for (let i = 0; i < K + 1; i++) {
        let tmp = [...cost];
        for (let [u, v, w] of flights) {
            tmp[v] = Math.min(tmp[v], cost[u] + w);
        }
        cost = tmp;
    }
    return cost[dst] === Infinity ? -1: cost[dst];
};

findCheapestPrice = function(n, flights, src, dst, K) {
    // build graph
    let graph = buildGraph(flights, n);
    let minCost = Infinity;
    // dfs
    let visited = new Array(n).fill(false);
    function dfs(src, hop, cost) {
        if (visited[src] || hop === K + 1 || src === dst || cost >= minCost) {
            if (src === dst) minCost = Math.min(minCost, cost);
            return;
        }
        visited[src] = true;
        for (let [adj, price] of graph[src])
            dfs(adj, hop + 1, cost + price);
        visited[src] = false;
    }
    // bfs
    function bfs() {
        let que = [[src, 0]];//[node, cost]
        let hop = 0;
        while (que.length > 0) {
            if (hop > K + 1) break;
            let nextQue = [];
            for (let [node, cost] of que) {
                if (node === dst || cost >= minCost) {
                    minCost = Math.min(minCost, cost);
                    continue;
                }
                for (let [adj, price] of graph[node]) {
                    nextQue.push([adj, cost + price]);
                }
            }
            que = nextQue;
            hop++;
        }
    }

    dfs(src, 0, 0);
    return minCost === Infinity ? -1 : minCost;
};

function buildGraph(flights, n) {
    let graph = new Array(n).fill(0).map(x => []);
    for (let [u, v, w] of flights) {
        graph[u].push([v, w]);
    }
    return graph;
}
```

---
## [Sentence Similarity II](https://leetcode.com/problems/sentence-similarity-ii/description/)

`有思路` `不熟练` `dfs` `uf`

1. dfs
> build graph from pairs and for each word pair, dfs graph and check if they are mutually reachable
> Time : O(|pairs| * |words1|) , build graph + traverse the whole graph for each word
> Space: O(|pairs|)
2. dfs + caching
> build graph + flood the graph while marking the ids for each foold + check each word
> Time :O(2 * |pairs| + |words1|)
> Space: O(|pairs|)
3. union & find
> build uf + check each word pair and see if they are in the same connected component
> TIme: O(|pairs| + |words1|)
> Space: O|pairs|)

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/737-ep118.png)

```javascript
var areSentencesSimilarTwo = function(words1, words2, pairs) {
    let m = words1.length, n = words2.length;
    if (m !== n) return false;
    //build graph
    let graph = buildGraph(pairs);
    //dfs
    function similar(node, target, visited) {
        if (node === target) return true;
        if (visited.has(node)) return false;
        visited.add(node);
        for (let adj of (graph.get(node) || [])) {
            if (similar(adj, target, visited)) return true;
        }
        return false;
    }
    for (let i = 0; i < m; i++) {
        if (!similar(words1[i], words2[i], new Set())) return false;    
    }
    return true;
};

areSentencesSimilarTwo = function(words1, words2, pairs) {
    let m = words1.length, n = words2.length;
    if (m !== n) return false;
    //build graph
    let graph = buildGraph(pairs);
    //build idMap
    let gid = 0, idMap = new Map(); //map <string->id>
    function mark(node, id) {
        if (idMap.has(node)) return;
        idMap.set(node, id);
        for (let adj of (graph.get(node) || [])) mark(adj, id);
    }
    for (let node of graph.keys()) {
        if (!idMap.has(node)) mark(node, gid++);
    }
    // check similarity
    for (let i = 0; i < m; i++) {
        let [w1, w2] = [words1[i], words2[i]];
        // let [id1, id2] = [w1, w2].map(x => (idMap.get(x) || -1)); //bug, get-> 0
        const similar = (w1, w2) => idMap.has(w1) && idMap.has(w2) && idMap.get(w1) === idMap.get(w2);
        if (w1 !== w2 && !similar(w1, w2)) return false;
    }

    return true;
};

function buildGraph(pairs) {
    //build graph
    let graph = new Map();
    for (let [w1, w2] of pairs) {
        if (!graph.has(w1)) graph.set(w1, []);
        if (!graph.has(w2)) graph.set(w2, []);
        graph.get(w1).push(w2);
        graph.get(w2).push(w1);
    }
    return graph;
}

class UF {
    constructor() {
        this.parents = new Map();//{string: string}
    }
    find(x) {
        let parents = this.parents;
        if (!parents.has(x) || parents.get(x) === x) {
            parents.set(x, x);
            return x;
        }
        // parent has x
        let px = this.find(parents.get(x));
        parents.set(x, px);
        return px;
    }
    union(x, y) {
        let [px, py] = [x, y].map(a => this.find(a));
        if (px === py) return;
        this.parents.set(px, py);
        return;
    }
}

areSentencesSimilarTwo = function(words1, words2, pairs) {
    //sanity check
    let m = words1.length, n = words2.length;
    if (m !== n) return false;
    //union
    let uf = new UF();
    for (let [w1, w2] of pairs) uf.union(w1, w2);
    //check similarity
    for (let i = 0; i < m; i++) {
        let [w1, w2] = [words1[i], words2[i]];
        if (uf.find(w1) !== uf.find(w2)) return false;    
    }
    return true;
};
```
---

## [clone graph](https://leetcode.com/problems/clone-graph/)

> dfs traverse the nodes
> for every node, create a copy, and then recursively populate its neighbors by calling clone graph on the neighbors

> `how to dfs`
> if (node is null) return null, nothing to copy
> if (node has been visited) all the copy has been done so no need to dfs it again, simply return its copy.
// this node hasn't been visited yet
> first create a copy of it. and populate the neighbor of it's copy by dfs through the neighbors.
> `each dfs does two things`
> 1. create a copy of the node
> 2. connect the neighbors via dfs through the neighbors


> bfs is more tedious , use map as both representation for edges and visited map. Only push to que the unvisited nodes
> `how to bfs`
> each bfs does the similar things copy the nodes if necessary & connect to it's neighbors and bfs through the unvisited neighbors.

```javascript
var cloneGraph = function(graph) {
    let map = new Map();
    function clone(node) {
        if (!node) return null;
        if (map.has(node)) return map.get(node);
        let copyNode = new UndirectedGraphNode(node.label);
        map.set(node, copyNode);
        for (let neighbor of node.neighbors) {
            copyNode.neighbors.push(clone(neighbor));
        }
        return copyNode;
    }
    return clone(graph);
};

var cloneGraph = function(graph) {
    if (!graph) return null;
    let map = new Map();
    let que = [graph];
    while (que.length > 0) {
        let node = que.shift();
        if (!map.has(node)) {
            map.set(node, new UndirectedGraphNode(node.label));
        }
        let clonedNode = map.get(node);
        for (let neighbor of node.neighbors) {
            if (!map.has(neighbor)) {
                map.set(neighbor, new UndirectedGraphNode(neighbor.label));
                que.push(neighbor);
            }
            let clonedNeighbor = map.get(neighbor)
            clonedNode.neighbors.push(clonedNeighbor);
        }
    }
    return map.get(graph);
};
```

---

## [graph valid tree](https://leetcode.com/problems/graph-valid-tree/description/)

1. make sure #edge = #node - 1
2. make sure no cycle

1 + 2 -> every node is connected as a tree
can use `uf` `dfs` `bfs` to detect cycle

> dfs/bfs graph, 如果存在cycle，那么最后遍历的node数量要小于#node
`if (visited.has(neighbor)` 要做的是continue而不是return false。
因为是undirected graph， each edge has two directions。 visited存在的不一定是cycle

> 用uf detect cycle 比较简单，if two nodes share the same connection component already, and they're being connect again, that means there is a cycle.

```javascript
var validTree = function(n, edges) {
    // 1) make sure #edge = #node - 1
    if (edges.length !== n - 1) return false;
    // 2) make sure no cycle
    // 1) + 2) => every node is connected as a tree
    let uf = new UF(n);
    for (let [u, v] of edges) {
        if (!uf.union(u, v)) return false;
    }
    return true;
};

class UF {
    constructor(size) {
        this.parents = [...Array(size).keys()];
    }
    find(x) {
        return x === this.parents[x] ? x : this.find(this.parents[x]);
    }
    union(x, y) {
        let px = this.find(x), py = this.find(y);
        if (px === py) return false; //detect cycle
        this.parents[px] = py;
        return true;
    }
}


var validTree = function(n, edges) {
    if (edges.length !== n - 1) return false;
    let adjs = createAdjs(n, edges);
    let visited = new Set();
    bfs(adjs, 0, visited);
    return visited.size === n;
};

var validTree = function(n, edges) {
    if (edges.length !== n - 1) return false;
    let adjs = createAdjs(n, edges);
    let visited = new Set();
    dfs(adjs, 0, visited);
    return visited.size === n;
};

function bfs(adjs, node, visited) {
    let que = [0];
    visited.add(0);
    while (que.length > 0) {
        let node = que.shift();
        for (let neighbor of adjs[node]) {
            if (visited.has(neighbor)) continue;
            visited.add(neighbor);
            que.push(neighbor);
        }
    }
};

function dfs(adjs, node, visited) {
    if (visited.has(node)) return;
    visited.add(node);
    for (let neighbor of adjs[node]) {
        dfs(adjs, neighbor, visited);
    }
}

function createAdjs(n, edges) {
    let adjs = new Array(n).fill(0).map(x => []);
    for (let [from, to] of edges) {
        adjs[from].push(to);
        adjs[to].push(from);
    }
    return adjs;
}
// 如果 edges # is not constrained, than the general approach of cycle detection
validTree = function(n, edges) {
    if (edges.length !== n - 1) return false;
    let map = new Map();
    for (let [s, e] of edges) {
        if (!map.has(s)) map.set(s, new Set());
        if (!map.has(e)) map.set(e, new Set());
        map.get(s).add(e);
        map.get(e).add(s);
    }
    let keys = [...map.keys()];
    let que = keys.length > 0 ? [keys[0]] : [], visited = new Set(que);
    while (que.length > 0) {
        let s = que.pop();
        for (let e of map.get(s)) {
            if (visited.has(e)) return false;
            visited.add(e);
            map.get(e).delete(s);
            que.push(e);
        }
    }
    return true;
};
```
---

## [acccounts merge](https://leetcode.com/problems/accounts-merge/description/)

> 这题结合了 UF/DFS and hashmap.
> 2 stages = graph building + dfs each connected component
or UF building + iterate through connected component

> use email2Name both as a hashmap and a uniq set to start 2nd stage (either dfs or uf)
> for UF, it's important to have a id distributor to distribute the ids to each email in a round robin fashion.

```javascript
var accountsMerge = function(accounts) {
    let adjs = new Map(); //edges of the graph
    let email2name = new Map();
    // build the graph and email2name mapping
    for (let account of accounts) {
        let name = account.shift();
        for (let i = 0; i < account.length; i++) {
            let email1 = account[i];
            email2name.set(email1, name);
            for (let j = i + 1; j < account.length; j++) {
                let email2 = account[j];
                if (!adjs.has(email1)) adjs.set(email1, new Set());
                if (!adjs.has(email2)) adjs.set(email2, new Set());
                adjs.get(email1).add(email2);
                adjs.get(email2).add(email1);
            }
        }
    }
    // dfs
    //let keys = [...adjs.keys()]; //bug1 ajds.keys only contains those nodes with neighbors
    let merged = [];
    let visited = new Set();
    for (let email of email2name.keys()) {
        if (!visited.has(email)) {
            let emails = [];
            dfs(adjs, email, emails, visited);
            merged.push([email2name.get(email), ...emails.sort()]);
        }
    }
    return merged;
};

function dfs(adjs, email, emails, visited) {
    if (visited.has(email)) return;
    visited.add(email);
    emails.push(email);
    //bug2 some nodes are isolated without edges
    for (let neighbor of (adjs.get(email) || [])) dfs(adjs, neighbor, emails, visited);
}

class UF {
    constructor() {
        this.parent = new Array(10001);
        for (let i = 0; i <= 10000; i++) this.parent[i] = i;
    }
    find(x) {
        if (this.parent[x] === x) return x;
        this.parent[x] = this.find(this.parent[x]);
        return this.parent[x];
    }
    union(x, y) {
        this.parent[this.find(x)] = this.find(y);
    }
}

accountsMerge = function(accounts) {
    let uf = new UF();
    let email2Name = new Map(), email2ID = new Map();
    let id = 0;
    for (let account of accounts) {
        let name = account.shift();
        let rootEmail = account[0];
        for (let email of account) {
            email2Name.set(email, name);
            if (!email2ID.has(email)) email2ID.set(email, id++);
            let [rootId, idx] = [rootEmail, email].map(key => email2ID.get(key));
            uf.union(rootId, idx);
        }
    }

    let merged = new Map();
    for (let email of email2Name.keys()) {
        let id = uf.find(email2ID.get(email));
        if (!merged.has(id)) merged.set(id, []);
        merged.get(id).push(email);
    }
    return [...merged.values()].map(emails => [email2Name.get(emails[0]), ...emails.sort()]);
};
```

---

## [alien dictionary](https://leetcode.com/problems/alien-dictionary/description/)

> using toplogical sort.
> stage1: building the indegree and out edges
> stage2: topological sort using bfs.

> use both map (char -> a set of src & dests) for indegree & outdegree.
because during building topology, same edge can appear mutiple times. when two words differ in any of the middle chars, it means we've found an order between the two char, connect them with a directed edge.

> then topological sort the graph and see if we're able to traverse all the nodes without running into a cycle.

```javascript
var alienOrder = function(words) {
    let [ins, outs] = buildTopology(words);
    let que = [];
    let chars = [...ins.keys()];
    for (let c of chars) {
        if (ins.get(c).size === 0) que.push(c);
    }
    let order = [];
    while (que.length > 0) {
        let c = que.shift();
        order.push(c);
        for (let neighbor of outs.get(c)) {
            ins.get(neighbor).delete(c);
            if (ins.get(neighbor).size === 0) que.push(neighbor);
        }
    }
    if (order.length === chars.length) return order.join('');
    return '';
};

function buildTopology(words) {
    let ins = new Map(), outs = new Map();
    for (let word of words) {
        for (let c of word) {
            //bug1 same edge can appear mutiple times
            ins.set(c, new Set());
            outs.set(c, new Set());
        }
    }
    for (let i = 0; i < words.length; i++) {
        for (let j = i + 1; j < words.length; j++) {
            let word1 = words[i], word2 = words[j];
            for (let k = 0; k < word1.length && k < word2.length; k++) { //bug3 forget to check word2len
                if (word1[k] !== word2[k]) {
                    ins.get(word2[k]).add(word1[k]);
                    outs.get(word1[k]).add(word2[k]);
                    break; //bug2 forget to break
                }
            }
        }
    }
    return [ins, outs];
}
```

---
