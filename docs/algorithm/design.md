# Design

## TicTacToe

```javascript
// Design and build the board game tic-tac-toe.  Please use real code, no pseudo code please
//   0. Understand the game mechanics: https://upload.wikimedia.org/wikipedia/commons/a/ae/Tic_Tac_Toe.gif
//   1. Pick best data structure to best store a game board
//   2. Write methods for:  setup game, making a move, check winner, error checking
//   3. Game is over when there is a winning hand (3 across, 3 down, or 3 of same diagonally)
class TicTacToe {
    constructor() {
        //player 1 -> +1 , player 2 -> -1
        this.board = new Array(3).fill(0).map(x => new Array(3).fill(0));
        this.cols = new Array(3).fill(0);
        this.rows = new Array(3).fill(0);
        this.diag = 0;
        this.antiDiag = 0;
    }
    // player: Number
    // r: row
    // c: col
    // return: Boolean
    // player1 : -1, player2: 1
    move(player, r, c) {
        if (this.board[r][c] !== 0) return false;
        this.board[r][c] = player;
        this.cols[c] += player;
        this.rows[r] += player;
        const isDiag = (i, j) => i + j === 2;
        const isAntiDiag = (i, j) => i === j;
        if (isDiag(r, c)) this.diag += player;
        if (isAntiDiag(r, c)) this.antiDiag += player;
        return true;
    }

    checkWinner() {
        const PLAYER1 = -1, PLAYER2 = 1;
        for (let row of this.rows) {
            if (row === -3) return PLAYER1;
            if (row === 3) return PLAYER2;
        }
        for (let col of this.cols) {
            if (col === -3) return PLAYER1;
            if (col === 3) return PLAYER2;
        }
        if (this.diag === -3) return PLAYER1;
        if (this.diag === 3) return PLAYER2;
                if (this.antiDiag === -3) return PLAYER1;
        if (this.antiDiag === 3) return PLAYER2;
        return 0;
    }
    print() {
        console.log('board');
        for (let i = 0; i < 3; i++) {
            console.log(this.board[i]);
        }
        console.log('rows');
        console.log(this.rows);

        console.log('cols');
        console.log(this.cols);

        console.log('diag');
        console.log(this.diag);

        console.log('antidiag');
        console.log(this.antiDiag);
    }
}

let ticTacToe = new TicTacToe();
ticTacToe.print();
const PLAYER1 = -1, PLAYER2 = 1;
ticTacToe.move(PLAYER1, 0, 0);
ticTacToe.print();
console.log('winner: ', ticTacToe.checkWinner());
ticTacToe.move(PLAYER1, 0, 1);
ticTacToe.move(PLAYER1, 0, 2);
ticTacToe.print();
console.log('winner: ', ticTacToe.checkWinner());
```

---

## [LRU cache](https://leetcode.com/problems/lru-cache/description/)

![](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/146-ep50.png)

```javascript
class ListNode {
    constructor(key, val) {
        this.key = key;
        this.val = val;
        this.prev = this.next = null;
    }
}

class List {
    constructor() {
        this.head = new ListNode();
        this.tail = new ListNode();
        [this.head.next, this.tail.prev] = [this.tail, this.head];
    }
    insertBack(node) {
        let [prev, next] = [this.tail.prev, this.tail];
        [prev.next, node.next] = [node, next];
        [node.prev, next.prev] = [prev, node];
    }
    remove(node) {
        let [prev, next] = [node.prev, node.next];
        [prev.next, next.prev] = [next, prev];
    }
    removeFront() {
        let node = this.head.next;
        this.remove(node);
        return node;
    }
}

var LRUCache = function(capacity) {
    this.capacity = capacity;
    this.map = new Map();
    this.list = new List();
};

LRUCache.prototype.get = function(key) {
    if (!this.map.has(key)) return -1;
    let node = this.map.get(key);
    this._touch(node);
    return node.val;
};

LRUCache.prototype._touch = function(node) {
    this.list.remove(node);
    this.list.insertBack(node);
};

LRUCache.prototype.put = function(key, value) {
    if (this.map.has(key)) {
        let node = this.map.get(key);
        node.val = value;
        this._touch(node);
        return;
    }
    if (this.map.size === this.capacity) {
        let node = this.list.removeFront();
        this.map.delete(node.key);
    }
    let node = new ListNode(key, value);
    this.list.insertBack(node);
    this.map.set(key, node);
};
```

---

## [LFU cache](https://leetcode.com/problems/lfu-cache/description/)

![](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/460-ep54-2.png)

![](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/460-ep54-3.png)

![](https://static.notion-static.com/d6c3843a-9660-4536-a97e-8b5c561f2ca2/Screen_Shot_2018-01-03_at_3.29.40_PM.png)

```
这题也可以用Priority Que或者balanced BST来做
Priority Que : GET O(n) SET O(n), <- touch O(n) because of the need to remove a specific node
BST (balanced) : GET O(lgn) SETO(lgn), <- touch O(lgn) insert , remove O(lgn)

这题和LRU有相似处。二者都是用hashmap作为主体，用一个维持order的数据结构来执行eviction policy，
对于LRU，linkedilst完全可以表达recency的order。
对于LFU，这个order = freq + recency, 可以用 heap or Balanced BST 来表示这个order.
也可以用 freqArray + linkedlist 来分层表示这个order.

when there is a tie (i.e., two or more keys that have the same frequency), the least recently used key would be evicted. 此处可以用到LRU的双向链表来达到O(1)时间的evict.
那么如何做到O(1)时间的LFU呢？用HashMap : freq -> freqNode , freqNodes are linked in LRU fashion.
use a global minFreq to keep track of the minFreq.

CacheNode(key, val, freq, freqNode)
FreqNode(key) // nodes in the LRU list

Get: O(1)
//remove old freq
use key to get the cacheNode(which contains the freq and freqNode)
find the freqList by freq, remove the freqNode from the freqList
if the freqList is empty after removal , delete the freqList from the freqMap.
if the freq to be deleted is the minFreq, update minFreq + 1

//update freq && insert newFreq
find the newFreqList (create it in the freqMap if necessary)
insert the new freq to the newFreqList

return cacheNode.val
Get操作对cacheMap没有改变，只是改变了cacheNode内部的freqNode，将其在freqMap以及freqList当中的顺序更新了，我们可以把这一系里更新抽象成touch操作

PUT O(1)
如果cacheMap有key， 那么更新cacheNode.val 然后touch更新LFU & LRU信息

如果cache已满，那么从minFreq的freqList中移除oldest freqNode， 这个时候freqNode.key 发挥作用，可以找到cacheMap的entry，移除他。
不用担心freqList变成空&&minFreq is gone的情况，因为很快我们就会将minFreq变成1，1就是新的minFreq，只有freqMap清不清空entry其实不重要，因为cacheMap可以保证不会访问到不存在的freq.

产生新的freqNode，然后新的cacheNode with freq = 1, 然后找到相应的freqList插入，更新freqMap和cacheMap
```

```javascript
class ListNode {
    constructor(key, val, used, tick) {
        this.key = key;
        this.val = val;
        this.used = used;
        this.tick = tick;
    }
}
var LFUCache = function(capacity) {
    this.map = new Map();
    this.heap = new Heap((a, b) => {
        if (a === b) return 0;
        if (a.used < b.used || (a.used === b.used && a.tick < b.tick)) return -1;
        return 1;
    }); //min Heap
    this.capacity = capacity;
    this.tick = 0;
};

/**
 * @param {number} key
 * @return {number}
 */
LFUCache.prototype.get = function(key) {
    if (!this.map.has(key)) return -1;
    let node = this._getNode(key);
    return node.val;
};

/**
 * @param {number} key
 * @param {number} value
 * @return {void}
 */
LFUCache.prototype.put = function(key, value) {
    if (this.capacity === 0) return;
    if (this.map.has(key)) {
        let node = this._getNode(key);
        node.val = value;
        return;
    }
    if (this.map.size === this.capacity) {
        let minNode = this.heap.pop();
        this.map.delete(minNode.key);
    }
    let node = new ListNode(key, value, 1, this.tick++);
    this.map.set(node.key, node);
    this.heap.push(node);
};

LFUCache.prototype._getNode = function(key) {
    let node = this.map.get(key);
    // update heap
    this.heap.remove(node);
    node.used++;
    node.tick = this.tick++;
    this.heap.push(node);
    return node;
};
```

```javascript
class CacheNode {
    constructor(key, val, freq, freqNode) {
        this.key = key;
        this.val = val;
        this.freq = freq;
        this.freqNode = freqNode;
    }
}
class FreqNode {
    constructor(key) {
        this.key = key;
        this.prev = this.next = null;
    }
}
class FreqList {
    constructor() {
        this.head = new FreqNode();
        this.tail = new FreqNode();
        [this.head.next, this.tail.prev] = [this.tail, this.head];
        this.size = 0;
    }
    insertBack(node) {
        let [prev, next] = [this.tail.prev, this.tail];
        [prev.next, node.next] = [node, next];
        [node.prev, next.prev] = [prev, node];
        this.size++;
    }
    removeFront() {
        let node = this.head.next;//LRU node
        this.remove(node);
        return node;
    }
    remove(node) {
        let [prev, next] = [node.prev, node.next];
        [prev.next, next.prev] = [next, prev];
        this.size--;
    }

}
/**
 * @param {number} capacity
 */
var LFUCache = function(capacity) {
    this.capacity = capacity;
    this.map = new Map(); // key -> CacheNode
    this.freqMap = new Map();
    this.minFreq = 0;
};

/**
 * @param {number} key
 * @return {number}
 */
LFUCache.prototype.get = function(key) {
    if (!this.map.has(key)) return -1;
    let cacheNode = this.map.get(key);
    this._touch(cacheNode);
    return cacheNode.val;
};

LFUCache.prototype._touch = function(node) {
    // update the freq
    let prevFreq = node.freq;
    node.freq++;

    // remove the node from the old freq list
    let freqList = this.freqMap.get(prevFreq);
    let freqNode = node.freqNode;
    freqList.remove(freqNode);

    if (freqList.size === 0 ) {
        this.freqMap.delete(prevFreq);
        if (prevFreq === this.minFreq) this.minFreq++;
    }

    // insert the key to the end of the new freqlist
    if (!this.freqMap.has(node.freq)) this.freqMap.set(node.freq, new FreqList());
    this.freqMap.get(node.freq).insertBack(freqNode);
};
/**
 * @param {number} key
 * @param {number} value
 * @return {void}
 */
LFUCache.prototype.put = function(key, value) {
    if (this.capacity === 0) return;
    if (this.map.has(key)) {
        let cacheNode = this.map.get(key);
        cacheNode.val = value;
        this._touch(cacheNode);
        return;
    }
    if (this.map.size === this.capacity) {
        // remove the element from the minFreq list
        let freqNode = this.freqMap.get(this.minFreq).removeFront();
        // remove the key from cache
        this.map.delete(freqNode.key);
    }
    this.minFreq = 1;
    let freqNode = new FreqNode(key);
    let node = new CacheNode(key, value, 1, freqNode);
    if (!this.freqMap.has(node.freq)) this.freqMap.set(node.freq, new FreqList());
    this.freqMap.get(node.freq).insertBack(freqNode);
    this.map.set(key, node);
};
```

---

## [read N characters given read 4](https://leetcode.com/problems/read-n-characters-given-read4/description/)

The read function will only be called once for each test case.

用一个大小为4的tmp buffer array来搬运character，一次进货 size个 (size <= 4) .  
卸货的时候要注意 保证 result buffer的cnt 不能超过n

```
while (cnt < n) {
//进货
//卸货
}
```

```javascript
var solution = function(read4) {
    /**
     * @param {character[]} buf Destination buffer
     * @param {number} n Maximum number of characters to read
     * @return {number} The number of characters read
     */
    return function(buf, n) {
        let buf4 = new Array(4).fill(0);
        let cnt = 0, eof = false;
        while (cnt < n && !eof) {
            let readCnt = read4(buf4);
            if (readCnt < 4) eof = true;
            for (let i = 0; cnt < n && i < readCnt; i++) buf[cnt++] = buf4[i];
        }
        return cnt;
    };
};
```
---

## [read N characters given read4 II - call multiple times](https://leetcode.com/problems/read-n-characters-given-read4-ii-call-multiple-times/description/)

The read function may be called multiple times.

which means we need to keep track of the current position of buf4.

```
while (cnt < n) {
	// 看情况要不要进货
	// 卸货
}
```

卸货的过程 要用到buf4的指针，从上次调用之后的位置开始卸货.
卸货之后如果buf4 empty, 需要充值buf4指针为0，为下一次进货做准备

```javascript
var solution = function(read4) {
    /**
     * @param {character[]} buf Destination buffer
     * @param {number} n Maximum number of characters to read
     * @return {number} The number of characters read
     */
    let buf4 = new Array(4).fill(0);
    let cnt4 = 0;
    let idx = 0;

    return function(buf, n) {
        let cnt = 0, eof = false;
        while (cnt < n && !eof) {
           if (idx === cnt4) {
               idx = 0;
               cnt4 = read4(buf4);
               if (cnt4 < 4) eof = true;
           }
           while (idx < cnt4 && cnt < n) buf[cnt++] = buf4[idx++];
        }
        return cnt;
    };
};
```
---

## [random pick index](https://leetcode.com/problems/random-pick-index/description/)

```
在不知道数组大小的情况下，以同等概论做出选择

reservior sampling 一定要讲数组遍历完毕，因为 最后的概率应该是 1/n 而不是 1 / i

The probability the that we will pick target at ith idx when the total number of element with value target is n > i . i could be 0 ~  n -1

P(i) = (1 / i) * (i / i + 1) * (i + 1 / i + 2) ... (n - 1 / n) = 1 / n
即在ith idx运气好了被选中，然后在之后的选举中运气好没被踢下来
```

```javascript
public class Solution {
    int[] nums;
    Random rand;
    public Solution(int[] nums) {
        this.nums = nums;
        this.rand = new Random();
    }
    public int pick(int target) {
        int total = 0;
        int res = -1;
        for (int i = 0; i < nums.length; i++) {
            if (nums[i] == target) {
                int x = rand.nextInt(++total);
                res = x == 0 ? i : res;
            }
        }
        return res;
    }
```

---

## [insert delete getrandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/description/)

insert O(1) & remove O(1) => hashset
getRandom O(1) => array
use array to store value, use hashmap to store value->index mapping
insert: append to the end of the dynamic array + add (val, idx) to the map
remove: remove val -> idx from the hashmap, remove idx from array by swapping the idx with the last element and pop
getRandom, pick a random number ranging from [0, n) and return the value on that idx.

```javascript
var RandomizedSet = function() {
    this.map = new Map(); //val -> idx in the arr
    this.arr = [];
};

RandomizedSet.prototype.insert = function(val) {
    if (this.map.has(val)) return false;
    this.map.set(val, this.arr.length);
    this.arr.push(val);
    return true;
};

RandomizedSet.prototype.remove = function(val) {
    if (!this.map.has(val)) return false;
    let idx = this.map.get(val);
    let last = this.arr.length - 1;
    if (idx < last) {
        this.arr[idx] = this.arr[last];
        this.map.set(this.arr[idx], idx);
    }
    this.map.delete(val);
    this.arr.pop();
    return true;
};

RandomizedSet.prototype.getRandom = function() {
    let i = ~~(this.arr.length * Math.random());
    return this.arr[i];
};
```

```
// step1: design add = O(1), remove O(1), removeRandom, O(N).
class RandomSet {
    constructor() {
        this.set = new Set();
    }
    add(val) {
        if (this.set.has(val)) return false;
        this.set.add(val);
        return true;
    }
    remove(val) {
        if (!this.set.has(val)) return false;
        this.set.delete(val);
        return true;
    }
    removeRandom() {
        if (this.set.size === 0) return false;
        let removeIndex = ~~(Math.random() * this.set.size);
        let i = 0;
        for (let val of this.set) {
            if (i === removeIndex) this.set.delete(val);
            i++;
        }
        return true;
    }

}
// step2: design add = O(1), remove O(N), removeRandom, O(1).
class RandomSetII {
    constructor() {
        this.arr = [];
    }
    add(val) { // O(1)
        this.arr.push(val);
    }
    remove(val) { // O(n)
        for (let i = 0; i < this.arr.length; i++) {
            if (this.arr[i] === val) {
                this.arr.splice(i, 1);
                break;
            }
        }
    }
    removeRandom() { // O(1)
        let i = ~~(Math.random() * this.arr.size);
        [this.arr[i], this.arr[this.arr.length - 1]] = [this.arr[this.arr.length - 1], this.arr[i]];
        this.arr.pop();
    }

}


// step3: design add = O(1), remove O(1), removeRandom, O(1).
class RandomSetIII {
    constructor() {
        this.arr = [];
        this.map = new Map();
    }
    add(val) { // O(1)
        this.map.set(val, this.arr.length);
        this.arr.push(val);
    }
    remove(val) { // O(1)
        if (!this.map.has(val)) return;
        let i = this.map.get(val);
        this._remove(i);
    }
    _remove(i) {
        let val = this.arr[i];
        this.map.set(this.arr[this.arr.length - 1], i);
        [this.arr[i], this.arr[this.arr.length - 1]] = [this.arr[this.arr.length - 1], this.arr[i]];
        this.arr.pop();
        this.map.delete(val);
    }
    removeRandom() { // O(1)
        let i = ~~(Math.random() * this.arr.size);
        this._remove(i);
    }

}

class RandomSetIV {
    constructor() {
        this.arr = [];
        this.map = new Map();
    }
    add(val) { // O(1)
        if (!this.map.has(val)) this.map.set(val, new Set());
        this.map.get(val).add(this.arr.length);
        this.arr.push(val);
    }
    remove(val) { // O(1)
        if (!this.map.has(val)) return false;
        let i = this.map.get(val).values().next().value;
        this._remove(i);
    }
    _remove(i) {
        let val = this.arr[i];
        let lastVal = this.arr[this.arr.length - 1];
        if (i < this.arr.length - 1) {
            this.arr[i] = lastVal;
            this.map.get(lastVal).delete(this.arr.length - 1);
            this.map.get(lastVal).add(i);
        }
        this.arr.pop();
        this.map.get(val).delete(i);
        if (this.map.get(val).size === 0) {
            this.map.delete(val);
        }
    }
    removeRandom() { // O(1)
        let i = ~~(Math.random() * this.arr.length);
        this._remove(i);
    }

}
```

---

## [two sum iii](https://leetcode.com/problems/two-sum-iii-data-structure-design/description/)

```javascript
var TwoSum = function() {
    this.cntMap = new Map();
    this.nums = [];
};

/**
 * Add the number to an internal data structure..
 * @param {number} number
 * @return {void}
 */
TwoSum.prototype.add = function(number) {
    this.nums.push(number);
    this.cntMap.set(number, (this.cntMap.get(number) || 0) + 1);
};

/**
 * Find if there exists any pair of numbers which sum is equal to the value.
 * @param {number} value
 * @return {boolean}
 */
TwoSum.prototype.find = function(value) {
    for (let num of this.nums) {
        let target = value - num;
        if (this.cntMap.has(target) && (target !== num || this.cntMap.get(target) > 1)) return true;
    }
    return false;
};
```
