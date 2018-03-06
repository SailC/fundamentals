# Google
## [Sqrt(x)](https://leetcode.com/problems/sqrtx/description/)
`有思路` `一遍过`

1. brute force `O(sqrt(x))`
> for i in [0, x], find the last i so that `i ^ 2 <= x`.
2. binary search `O(lg(n))`
> predicate `f(x) <=> x ^ 2 <= target`
`true, true, true, ..., false, false, false`
find the last x so that f(x) is true.
小心`lo = mid` 容易引起死循环
`mid = lo + ~~((hi - lo + 1) / 2)` to avoid dead loop
```javascript
var mySqrt = function(x) {
    let lo = 0, hi = x;
    while (lo < hi) {
        let mid = lo + ~~((hi - lo + 1) / 2);
        if (mid * mid > x) {
            hi = mid - 1;
        } else {
            lo = mid;
        }
    }
    return lo;
};
```
---
## [Sort Transformed Array](https://leetcode.com/problems/sort-transformed-array/description/)
`无思路` `双指针靠拢` `函数单调性`

1. brute force `O(nlgn)`
> `input.map(x => a * x * x + b * x + c).sort()`
2. two pointers `O(n)`
> 这里利用了二次函数的单调性，for a input x in [lo, hi], we maintain an invariant that the biggest/smallest value of window [lo, hi] always appear in one of the two boundaries.
> (1) If a > 0, the biggest f(x) must be either in index lo or hi.
> (2) If a < 0, the smallest f(x) must be either in index lo or hi.
> after picking the extreme value, we adjust the boundaries accordingly to update the current input window.
> (3) When a === 0, the function is a straight line so the above method still works.

```javascript
var sortTransformedArray = function(nums, a, b, c) {
    let n = nums.length, lo = 0, hi = n - 1;
    let newArr = new Array(n), i = a > 0 ? n - 1 : 0;
    const f = x => a * x * x + b * x + c;
    for (let _j = 0; _j < n; _j++) {
        if (a > 0) newArr[i--] = f(nums[lo]) > f(nums[hi]) ? f(nums[lo++]) : f(nums[hi--]);
        else newArr[i++] = f(nums[lo]) < f(nums[hi]) ? f(nums[lo++]) : f(nums[hi--]);
    }
    return newArr;
};
```
---
## [Insert Interval](https://leetcode.com/explore/interview/card/google/63/sorting-and-searching-4/445/)
`印象深刻` `一遍过` `interval`

1. binary insert the newInterval + merge intervals `O(nlgn)`
2. left Non-overlap + overlap + right Non-overlap `O(n)`
> (1) Add the left non-overlapped intervals to the result.
> (2) Merge the overlapped intervals with the new incoming interval.And push the merged interval to the result.
> (3) Add the right non-overlapped intervals to the result.

```javascript
var insert = function(intervals, newInterval) {
    let i = 0, n = intervals.length;
    let newIntervals = [];
    const overlap = (a, b) => !(a.start > b.end || a.end < b.start);
    while (i < n && intervals[i].end < newInterval.start) newIntervals.push(intervals[i++]);
    while (i < n && overlap(intervals[i], newInterval)) newInterval = new Interval(Math.min(intervals[i].start, newInterval.start), Math.max(intervals[i++].end, newInterval.end));
    newIntervals.push(newInterval);
    while (i < n) newIntervals.push(intervals[i++]);
    return newIntervals;
};
```
---
## [Merge Intervals](https://leetcode.com/problems/merge-intervals/description/)
`印象深刻` `一遍过` `interval`

We try to maintain a merged non-overlappign intervals in the new array as we're processing the input intervals.

1. bruteforce `O(n^2)`
> For each incoming interval `a` , scan all the already merged `b` intervals.
> `const overlap = (a, b) => !(a.start > b.end || a.end < b.start);`
>  (1) If non overlap, add the interval `b` to the next round merged intervals. 放心 Note that if the incomming interval doesn't overlap with interval `b`, then the merged new incomming interval won't overlap with `b` either because of the invariant.
>  (2) if overlap, create a new incomming interval by merging `a` and `b`
>  (3) after scanning all, push the new incomming interval to the next round intervals

2. sort `O(nlgn)`
> 为什么要按照 start sort? 因为这样 只需要考虑 upcomming.start 和 last.end 之间的关系，而不用对之前 interval 逐一判断overlap. O(n ^ 2) => O(nlgn)
> Maintain an invariant that the result contains merged intervals sorted by starting index. for a incoming interval, only need to consider the last interval because the previous interval is either merged or non overlapped. since new.start > last.start, we only consider the new.start and last.end and see if they're overlapped.

```javascript
var merge = function(intervals) {
    intervals.sort((a, b) => a.start - b.start);
    const overlap = (a, b) => !(a.start > b.end || a.end < b.start);
    const mergeInt = (a, b) => new Interval(Math.min(a.start, b.start), Math.max(a.end, b.end));
    let merged = [];
    for (let interval of intervals) {
        if (merged.length === 0 || !overlap(interval, merged[merged.length - 1])) {
            merged.push(interval);
        } else {
            let top = merged.pop();
            merged.push(mergeInt(top, interval));
        }
    }
    return merged;
};
```
---
## [Longest Palindromic Substring](https://leetcode.com/explore/interview/card/google/63/sorting-and-searching-4/451/)
`有思路` `有点生疏` `palindrome` `双指针扩散` `dp`

1. brute force `O(n ^ 3)`
> enumerate all `n ^ 2` substrings and check if they are palindrome.
2. dp `O(n ^ 2)`
> it would be great if we can perform palindrome check in `O(1)` time
> `dp[i][j] = i === j || i + 1 === j || (s[i] === s[j - 1] && dp[i + 1][j - 1]);`
3. middle out building palindromes `O(n ^ 2)`
> start building potential palindromes by extending two boundaries if possible

```javascript
var longestPalindrome = function(s) {
    let lo = 0, hi = 0, n = s.length;
    if (n === 0) return '';

    const middleOut = (lo, hi) => {
        while (lo >= 0 && hi < n && s[lo] === s[hi]) {
            lo--;
            hi++;
        }
        return [lo + 1, hi - 1];
    };

    for (let i = 0; i < n; i++) {
        let [start, end] = middleOut(i, i);
        if (end - start > hi - lo) [lo, hi] = [start, end];
        if (i < n - 1) {
            let [start, end] = middleOut(i, i + 1);
            if (end - start > hi - lo) [lo, hi] = [start, end];
        }
    }

    return s.slice(lo, hi + 1);
};

longestPalindrome = function(s) {
    let n = s.length, lo = 0, hi = 0;
    if (n === 0) return '';
    let dp = new Array(n + 1).fill(0).map(x => new Array(n + 1).fill(false));
    for (let i = n; i >= 0; i--) {
        for (let j = i; j <= n; j++) {
            dp[i][j] = i === j || i + 1 === j || (s[i] === s[j - 1] && dp[i + 1][j - 1]);
            if (dp[i][j] && j - i >= hi - lo) {
                lo = i;
                hi = j;
            }
        }    
    }
    return s.slice(lo, hi);
};
```
---
## [Diagonal Traverse](https://leetcode.com/problems/diagonal-traverse/description/)
`有思路` `代码脏` `矩阵模拟`

1. Simulation
> Only two directions, when `r + c % 2 === 0` moving `up_right`, else moving `down_left`
for each step, try to figure out the next step based on out of bound cases:
(1) if cur direction is moving up_right
(1.a) if next step causes both row & col out of bound or only causes col out of bound, move down
(1.b) if next step only causes row out of bound, move right
(1.c) if no out of bound, move up_right
(2) if cur direction is moving down_left
(2.a) if next step causes both row & col out of bound or only causes row out of bound, move right
(2.b) if next step only causes col out of bound, move down
(2.c) if no out of bound, move down_left

```javascript
var findDiagonalOrder = function(matrix) {
    if (matrix === null || matrix.length === 0) return [];

    let m = matrix.length, n = matrix[0].length;
    let r = 0, c = 0, result = [];

    for (let i = 0; i < m * n; i++) {
        result.push(matrix[r][c]);
        if ((r + c) % 2 === 0) { // moving up
            if (c === n - 1) r++;
            else if (r === 0) c++;
            else {
                r--;
                c++;
            }
        } else {//moving down
            if (r === m - 1) c++;
            else if (c === 0) r++;
            else {
                r++;
                c--;
            }
        }
    }


    return result;
};
```

## [Next Greater Element I](https://leetcode.com/problems/next-greater-element-i/description/)
`茅塞顿开` `stack`

1. bruteforce `O(m * n)`
> for each num in findNums, scan nums to find the next greater num by iterating from the beginning.
2. bruteforce + hashmap `O(m* n)`
> same idea plus using hashmap to save the index to start fiding the next greater num.
3. stack `O(m + n)`
> preprocess the next greater num in nums. Use stack (invariant: all the elements in the stack haven't met the next greater incoming num yet). (1) if incoming num is greater than the top of the stack, pop the stack, update top's next greater num, continue to do this until stack is empty or incoming num is <= top (2) put the incoming num to the stack , now the stack elements should meet the invariant again. (3) after scanning all the nums , if the stack is not empty, the remaining nums don't have next greater number.

```javascript
var nextGreaterElement = function(findNums, nums) {
    let indexMap = new Map();
    let n = nums.length;
    for (let i = 0; i < n; i++) indexMap.set(nums[i], i);

    const nextGreaterNum = x => {
        let idx = indexMap.get(x);
        for (let i = idx + 1; i < n; i++) {
            if (nums[i] > x) return nums[i];
        }
        return -1;
    }

    return findNums.map(nextGreaterNum)
};

nextGreaterElement = function(findNums, nums) {
    let map = new Map(), stack = [], n = nums.length;
    for (let i = 0; i < n; i++) {
        let num = nums[i];
        while (stack.length > 0 && stack[stack.length - 1] < num) {
            let top = stack.pop();
            map.set(top, num);
        }
        stack.push(num);
    }
    while (stack.length > 0) map.set(stack.pop(), -1);
    return findNums.map(x => map.get(x));
};
```

---
## [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/description/)

`有思路` `代码脏` `flooding` `bfs/dfs with matrix`

1. flooding with bfs / dfs
> Flooding from the 2 oceans (pacific & atlantic) to the land, use two 2d arrays to mark the floodable lands from 2 oceans. After flooding, pick the lands that are floodable by both oceans.
the 2d array for oceans can be used as visited set to prevent dead loop in the bfs / dfs.
对于flooding的dfs，visited backtrack的时候不需要重置. flooding的时候先check再移动，移动到某格就说明那一格是合法的，就要将其visited设置为true.

```javascript
var pacificAtlantic = function(matrix) {
    if (matrix === null || matrix.length === 0) return [];
    let m = matrix.length, n = matrix[0].length;
    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    let pac = new Array(m).fill(0).map(x => new Array(n).fill(false));
    let atl = new Array(m).fill(0).map(x => new Array(n).fill(false));

    const bfs = ocean => {
        let que = [];
        let visited = ocean === 'pac' ? pac : atl;
        if (ocean === 'pac') {
            for (let i = 0; i < m; i++) {
                que.push([i, 0]);
                visited[i][0] = true;
            }
            for (let i = 0; i < n; i++) {
                que.push([0, i]);
                visited[0][i] = true;
            }
        } else {
            for (let i = 0; i < m; i++) {
                que.push([i, n - 1]);
                visited[i][n - 1] = true;
            }
            for (let i = 0; i < n; i++) {
                que.push([m - 1, i]);
                visited[m - 1][i] = true;
            }
        }

        while (que.length > 0) {
            let [i, j] = que.shift();
            for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
                if (outOfBound(x, y) || visited[x][y] || matrix[x][y] < matrix[i][j]) continue;
                visited[x][y] = true;
                que.push([x, y]);
            }
        }
    };

    const dfs = (i, j, visited) => {
        visited[i][j] = true;
        for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
            if (outOfBound(x, y) || visited[x][y] || matrix[x][y] < matrix[i][j]) continue;
            dfs(x, y, visited);
        }
    };

    // populate pac & atl
    // for (let ocean of ['pac', 'alt']) bfs(ocean);
    for (let ocean of ['pac', 'alt']) {
        if (ocean === 'pac') {
            for (let i = 0; i < m; i++) dfs(i, 0, pac);
            for (let i = 0; i < n; i++) dfs(0, i, pac);
        } else {
            for (let i = 0; i < m; i++) dfs(i, n - 1, atl);
            for (let i = 0; i < n; i++) dfs(m - 1, i, atl);
        }
    }

    let result = [];
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (pac[i][j] && atl[i][j]) result.push([i, j]);
        }
    }
    return result;
};
```
---
## [Sentence Screen Fitting](https://leetcode.com/problems/sentence-screen-fitting/description/)

`没有思路` `字符串细节题` `循环index`

1. 我的想法
> 我刚开始想的是便利句子，每个单词分别处理，但是这种做法很不高效，因为有可能屏幕的宽度特别大，而单词可能就一两个，那么我们这样遍历的话就太浪费时间了，应该直接用宽度除以句子加上空格的长度之和，可以快速的得到能装下的个数
2. 指针移动
> 首先明确求解目标 `find how many times the given sentence can be fitted on the screen.` 我们可以把sentence 首尾相连看做一个无限长的字符串，单词中间用空格隔开，然后我们的目标是每次屏幕输出一行，我们就记录下下一行首个字符在无限长字符串的位置，这个位置其实就是之前所输出的所有sentence的总长度，最后除以一个句子的长度，就可以得到个数。
> (1) 中循环遍历屏幕每一行，每次试图col个char，增加start index的位置
> (2) 如果增加之后的start index的位置上是一个空格，则说明空格之前的单词正好可以放入该行不溢出，我们队start index++指向下一行首字符位置
> (3) 如果start index位置不是空格，说明当前试图输出的单词屏幕存不下，那么前移start index指向当前单词首字符
> (4) 无论如何，当当前行填充完毕之后，index的位置一定是下一行首字母的位置，也就是到目前为止已经在屏幕上输出的sentence总长。

```javascript
var wordsTyping = function(sentence, rows, cols) {
    sentence = sentence.join(' ') + ' ';
    let n = sentence.length;
    let j = 0;
    for (let i = 0; i < rows; i++) {
        j += cols;
        if (sentence[j % n] === ' ') j++;
        else {
            while (j > 0 && sentence[(j - 1) % n] !== ' ') j--;
        }
    }
    return ~~(j / n);
};
```

## [Maximum Vacaction Days](https://leetcode.com/problems/maximum-vacation-days/description/)

`套路` `代码脏` `dfs->dp`

1. Depth first search & backtracking
> use a recursive function `dfs`, which returns the max number of vacation days taken starting from `curCity` at `curWeek`.
> Note "You totally have K weeks (each week has 7 days) to travel. You can only take flights at most once per day and can only take flights on each week's Monday morning. Since flight time is so short, we don't consider the impact of flight time." which means on every Monday you can decide to either stay or fly to another city for the following week.
> Thus, for the current city, we choose different city as the next cities and find out the max number of vacation days we can get by flying to those cities for the following week.
> Time Complexity : `O(n ^ k)` . Depth of the recursion tree will be k and each node contains n branches in the worst case.

2. Dfs with memorization
> we make a number of redundant function calls, since the same function call of the form `dfs(cur_city, weekno)` can be made multiple number of times with the same `cur_city` and `weekno`. These redundant calls can be pruned off if we make use of memoization.
> Time Complexity: `O(n * n * k)`. memo array of size `n * k` is filled and each cell filling takes `O(n)` time

3. DP
> 之前用从前到后的 `dp[i][j]` 表示到week j 为止，人在city i的时候的max days，不过这样做不是很符合题意，因为city i不一定能过从city 0 飞过来，所以还是从后往前推，将`dp[i][j]` 表示为从week j开始人在city i的时候的max days。这样最后dp[0][0]就是所求解.
> 由于所有dp[i][j]都只依赖于dp[i'][j + 1], 所以可以用temp array记录下这一周的情况，一周一周更新一维dp数组.

```javascript

maxVacationDays = function(flights, days) {
    let n = flights.length, k = days[0].length;
    let cache = new Array(n).fill(0).map(x => new Array(k).fill(-1));

    function dfs(curCity, curWeek) {
        if (curWeek === k) return 0;
        if (cache[curCity][curWeek] !== -1) return cache[curCity][curWeek];
        let maxDays = 0;
        for (let i = 0; i < n; i++) {
            if (flights[curCity][i] === 1 || i === curCity) {
                let vacDays = days[i][curWeek] + dfs(i, curWeek + 1);
                maxDays = Math.max(maxDays, vacDays);
            }
        }
        cache[curCity][curWeek] = maxDays;
        return maxDays;
    }

    return dfs(0, 0);
};

var maxVacationDays = function(flights, days) {
    let n = flights.length, k = days[0].length;
    let dp = new Array(n).fill(0).map(x => new Array(k + 1).fill(0));
    for (let week = k - 1; week >= 0; week--) {
        for (let city = 0; city < n; city++) {
            for (let i = 0; i < n; i++) {
                if (i === city || flights[city][i] === 1) {
                    dp[city][week] = Math.max(dp[city][week], days[i][week] + dp[i][week + 1]);
                }
            }
        }
    }

    return dp[0][0];
};

maxVacationDays = function(flights, days) {
    let n = flights.length, k = days[0].length;
    let dp = new Array(n).fill(0);
    for (let week = k - 1; week >= 0; week--) {
        let tmp = new Array(n).fill(0);
        for (let city = 0; city < n; city++) {
            for (let i = 0; i < n; i++) {
                if (i === city || flights[city][i] === 1) {
                    tmp[city] = Math.max(tmp[city], days[i][week] + dp[i]);
                }
            }
        }
        dp = tmp;
    }

    return dp[0];
};
```

## [Edit Distance](./dp.md#edit-distance)
---
## [Minimum Path Sum](./dp.md#minimum-path-sum)
---
## [House Robber](./dp.md#house-robber)
---
## [House Robber II](./dp.md#house-robber-ii)
---
## [Moving Average from Data Stream](https://leetcode.com/problems/moving-average-from-data-stream/description/)

1. queue `O(1)` next
> if queue overflow, shift the oldest element out and deduct the value from the sum.
2. circular buffer `O(1)`
> we use circular index to refer to the next position to insert, when the buffer is full, we replace the oldest position with the new value. (FIFO order).

```javascript
var MovingAverage = function(size) {
    this.sum = 0;
    this.arr = [];
    this.size = size;
};

/**
 * @param {number} val
 * @return {number}
 */
MovingAverage.prototype.next = function(val) {
    this.arr.push(val);
    this.sum += val;
    if (this.arr.length > this.size) this.sum -= this.arr.shift();
    return this.sum / this.arr.length;
};

var MovingAverage = function(size) {
    this.sum = 0;
    this.arr = new Array(size);
    this.size = 0;
    this.idx = 0;
};

/**
 * @param {number} val
 * @return {number}
 */
MovingAverage.prototype.next = function(val) {
    if (this.size === this.arr.length) this.sum -= this.arr[this.idx];
    this.arr[this.idx] = val;
    this.sum += val;
    this.idx = (this.idx + 1) % this.arr.length;
    if (this.size < this.arr.length) this.size++;
    return this.sum / this.size;
};
```

## [Peeking Iterator](https://leetcode.com/problems/peeking-iterator/description/)
`无思路` `Design`

[tutorial es6 iterator & iterable](http://exploringjs.com/es6/ch_iteration.html)

1. cache
> cache the next element. when next is called, return the previously cached element and continue to cache the next element.

```javascript
class Iterable {
    constructor(...args) {
        this.args = args;
    }
	[Symbol.iterator]() {
		let index = 0, args = this.args;
		const iterator = {
            hasNext() {
                return index < args.length;  
            },
			next() {
                if (index < args.length) return {value: args[index++]};
                return {done: true};
            }
		};
		return iterator;
	}
}

class PeekIterable {
    constructor(iterator) {
        this.it = iterator;
    }
    [Symbol.iterator]() {
        let it = this.it;
        let hasNextEntry = it.hasNext();
        let nextEntry = hasNextEntry? it.next() : null;
        const iterator = {
            hasNext() {
                return hasNextEntry;  
            },
            peek() {
                return nextEntry;
            },
            next() {
                let result = nextEntry;
                hasNextEntry = it.hasNext();
                nextEntry = hasNextEntry? it.next() : null;
                return result;
            }
        }
        return iterator;
    }
}



let i = new Iterable(1,2,3);
console.log([...i]);
let pi = new PeekIterable(i[Symbol.iterator]());
let it = pi[Symbol.iterator]();

console.log(it.hasNext());
console.log(it.next());

console.log(it.hasNext());
console.log(it.peek());

console.log(it.hasNext());
console.log(it.next());

console.log(it.hasNext());
console.log(it.next());

console.log(it.hasNext());
console.log(it.next());
```
---
## [Binary Search Tree Iterator](https://leetcode.com/problems/binary-search-tree-iterator/description/)

`一遍过` `BST` `In order traversal` `stack`

1. in order traversal
> `next smallest number in BST` => `in order traversal`
> This is a application of the iterative inorder traversal. we need to make sure the next element poping from the stack is the next smallest one. which means all the previous smaller ones have all been processed.
> So for each newly process ones, we make sure the left branch has all been processed, and push the right subtree's left branch to the stack.

```javascript
var BSTIterator = function(root) {
    this.stack = [];
    for (let node = root; node; node = node.left) this.stack.push(node);
};


/**
 * @this BSTIterator
 * @returns {boolean} - whether we have a next smallest number
 */
BSTIterator.prototype.hasNext = function() {
    return this.stack.length > 0;
};

/**
 * @this BSTIterator
 * @returns {number} - the next smallest number
 */
BSTIterator.prototype.next = function() {
    let node = this.stack.pop();
    for (let cur = node.right; cur; cur = cur.left) this.stack.push(cur);
    return node.val;
};
```
---
## [Zigzag Iterator] (https://leetcode.com/problems/zigzag-iterator/description/)
`有思路` `iterator` `que`

1. index + buffer
> we use an index i to indicate the next row idx, and stores the col id for each row. each time we check if the col id is valid, if not we continue to the next row.

2. que + iterator
> Uses a que to store the iterators in different vectors. Every time we call next(), we pop an element from the list, and re-add the iterator to the end to cycle through the lists.

```javascript
var ZigzagIterator = function ZigzagIterator(v1, v2) {
    this.k = 2;
    this.i = 0;
    this.js = new Array(this.k).fill(0);
    this.vs = [v1, v2];
    this.n = v1.length + v2.length;
    this.cnt = 0;
};


/**
 * @this ZigzagIterator
 * @returns {boolean}
 */
ZigzagIterator.prototype.hasNext = function hasNext() {
    return this.cnt < this.n;
};

/**
 * @this ZigzagIterator
 * @returns {integer}
 */
ZigzagIterator.prototype.next = function next() {
    let [k, i, js, vs] = [this.k, this.i, this.js, this.vs];
    while (js[i] === vs[i].length) i = (i + 1) % k;
    this.i = i;
    let idx = js[i]++;
    this.cnt++;
    this.i = (this.i + 1) % k;
    return vs[i][idx];
};

var ZigzagIterator = function ZigzagIterator(v1, v2) {
    this.iterators = [v1, v2].map(x => x[Symbol.iterator]());
    this.n = v1.length + v2.length;
    this.cnt = 0;
};


/**
 * @this ZigzagIterator
 * @returns {boolean}
 */
ZigzagIterator.prototype.hasNext = function hasNext() {
    return this.cnt < this.n;
};

/**
 * @this ZigzagIterator
 * @returns {integer}
 */
ZigzagIterator.prototype.next = function next() {
    let its = this.iterators;
    while (true) {
        let it = its.shift();
        let next = it.next();
        if (!next.done) {
            its.push(it);
            this.cnt++;
            return next.value;
        }
    }
};
```
---
## [Design Tic-Tac-Toe](https://leetcode.com/problems/design-tic-tac-toe/)
`套路` `粗心` `matrix`

1.  sparse matrix
> The key observation is that in order to win Tic-Tac-Toe you must have the entire row or column. Thus, we don’t need to keep track of an entire n^2 board. We only need to keep a count for each row and column. If at any time a row or column matches the size of the board then that player has won.
> To keep track of which player, I add one for Player1 and -1 for Player2. There are two additional variables to keep track of the count of the diagonals. Each time a player places a piece we just need to check the count of that row, column, diagonal and anti-diagonal.

```javascript
/**
 * Initialize your data structure here.
 * @param {number} n
 */
var TicTacToe = function(n) {
    this.n = n;
    this.rows = new Array(n).fill(0),
    this.cols = new Array(n).fill(0),
    this.diag = 0,
    this.antiDiag = 0;
};

/**
 * Player {player} makes a move at ({row}, {col}).
        @param row The row of the board.
        @param col The column of the board.
        @param player The player, can be either 1 or 2.
        @return The current winning condition, can be either:
                0: No one wins.
                1: Player 1 wins.
                2: Player 2 wins.
 * @param {number} row
 * @param {number} col
 * @param {number} player
 * @return {number}
 */
TicTacToe.prototype.move = function(row, col, player) {
    let score = player === 1 ? 1: -1;
    let win = player === 1 ? this.n : -this.n;
    this.rows[row] += score;
    this.cols[col] += score;
    if (row + col === this.n - 1) this.diag += score;
    if (row === col) this.antiDiag += score;
    if (this.rows[row] === win || this.cols[col] === win || this.diag === win || this.antiDiag === win) return player;
    return 0;
};
```
---

## [utf-8-validation](https://leetcode.com/problems/utf-8-validation/description/)
1. bit manipulation + control flow
> 立一个flag cnt用来表示下一次字节应该是否应该当作首字符来处理.
> 如果是首字符，那么根据首字符的前几个bit来判断这个UTF-8字符串的字符个数.
> `10000000` 是非法字符串
> 如果不是首字符 , 那么如果不等于`10xxxxxx` 就是非法字符.

```javascript
var validUtf8 = function(data) {
    let cnt = 0;
    for (let d of data) {
        if (cnt === 0) {
            if ((d >> 5) === 0b110) {
                cnt = 1;
            } else if ((d >> 4) === 0b1110) {
                cnt = 2;
            } else if ((d >> 3) === 0b11110) {
                cnt = 3;
            } else if (d >> 7) {
                return false;
            }
        } else {
            if ((d >> 6) != 0b10) {
                return false;
            }
            cnt--;
        }
    }
    return cnt === 0;
};
```
---
## [Maximum Product of Word Lengths](https://leetcode.com/problems/maximum-product-of-word-lengths/description/)
`有思路` `bitmap`

1. bruteforce `O(n ^ 3)`
> for each pair of words, we check if they share any letter in `O(n)` time

2. bitmap `O(n ^ 2)`
> can we do the check with `O(1)` time, we can preprocess the words, map each of them to a bitmap indicating whether a char is used in the word. To check if two words overlap in some char, just & the two bitmap of the word.

```javascript
var maxProduct = function(words) {
    let cache = new Map();

    const word2bitmap = word => {
        if (cache.has(word)) return cache.get(word);
        let bitmap = 0;
        for (let c of word) bitmap |= (1 << (c.charCodeAt(0) - 'a'.charCodeAt(0)));
        cache.set(word, bitmap);
        return cache.get(word);
    };

    const shareLetter = (w1, w2) => (word2bitmap(w1) & word2bitmap(w2)) !== 0;

    let n = words.length, maxVal = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            if (!shareLetter(words[i], words[j])) maxVal = Math.max(maxVal, words[i].length * words[j].length);
        }
    }
    return maxVal;
};
```
---
## [Bold Words in String](https://leetcode.com/problems/bold-words-in-string/description/)

1. mark and sweep
> First, determine which letters are bold and store that information in mask[i] = if i-th character is bold. Then, insert the tags at the beginning and end of groups. The start of a group is if and only if (mask[i] and (i == 0 or not mask[i-1])), and the end of a group is similar.
> Sweep的时候巧妙的考察当前字符和前一个字符的关系来确定要不要加tag
> mark的时候可用set来优化时间复杂度
> Time: O(sLen * wordsLen * L) `L = max word length`
> 可优化为 O(sLen * L * L ) 这样的好处是如果words里面有overlap的话，不用对每一个word都mark一遍overlap的部分，而是从overlap出发，查看自己那部分在不在dict里面.
> 甚至可以再优化一下，每次mark(i, j) 区间的时候，j从后完全扫描，如果在dict里面，那么直接break

`有思路` `代码脏` `String` `hashset`

```javascript
var boldWords = function(words, S) {
    let n = S.length, bold = new Array(n).fill(false);

    // for (let word of words) {
    //     for (let i = 0; i + word.length <= n; i++) {
    //         if (word === S.slice(i, i + word.length)) {
    //             for (let j = i; j < i + word.length; j++) bold[j] = true;
    //         }
    //     }
    // }
    words = new Set(words);
    const MAX_WORD_LEN = 10;
    for (let i = 0; i < n; i++) {
        // for (let j = i + 1; j <= Math.min(n, i + MAX_WORD_LEN); j++) {
        for (let j = Math.min(n, i + MAX_WORD_LEN); j > i; j--) {
            let word = S.slice(i, j);
            if (words.has(word)) {
                for (let k = i; k < j; k++) bold[k] = true;
                break;
            }
        }
    }

    let boldS = [];
    for (let i = 0; i < n; i++) {
        if (bold[i] && (i === 0 || !bold[i - 1])) boldS.push('<b>');
        boldS.push(S[i]);
        if (bold[i] && (i === n - 1 || !bold[i + 1])) boldS.push('</b>');
    }
    return boldS.join('');
};
```

---

## [Find Anagram Mapping](https://leetcode.com/problems/find-anagram-mappings/description/)

`一遍过` `hashtable`

1.brute force `O(n ^ 2)`
> for each a, try to find a matching element in b by scanning
2. hashtable
> preprocess b to create value to index mapping
> if we want each a map to a different b , then we need a store indices of the same b as a list. and each time pop a index from that list

```javascript
var anagramMappings = function(A, B) {
    let map = new Map();
    for (let i = 0; i < B.length; i++) {
        let num = B[i];
        if (!map.has(num)) map.set(num, []);
        map.get(num).push(i);
    }
    let index = [];
    for (let num of A) {
        index.push(map.get(num).pop());
    }
    return index;
};
```
---
## [Largest Number At Least twice of others](https://leetcode.com/problems/largest-number-at-least-twice-of-others/description/)
`一遍过` `2pass`

1. two pass scan `O(N)`
> Scan through the array to find the unique largest element m, keeping track of it's index maxIndex.
> Scan through the array again. If we find some x != m with m < 2*x, we should return -1.
> Otherwise, we should return maxIndex.

```javascript
var dominantIndex = function(nums) {
    let n = nums.length;
    if (n === 0) return -1;
    let idx = 0;
    for (let i = 0; i < n; i++) {
        if (nums[i] > nums[idx]) idx = i;
    }
    for (let i = 0; i < n; i++) {
        if (i !== idx && nums[i] * 2 > nums[idx]) return -1;
    }
    return idx;
};
```
---
## [Shortest Completing Word](https://leetcode.com/problems/shortest-completing-word/description/)

`一遍过` `cntMap` `hashmap`

1. Compare counts `O(N * MAX_WORD_LEN)`
> We count the number of letters in both word and licensePlate, converting to lowercase and ignoring non-letter characters. If the count of each letter is greater or equal in the word, then that word completes the licensePlate.

```javascript
var shortestCompletingWord = function(licensePlate, words) {
    let cntMap = new Map();
    for (let c of licensePlate) {
        c = c.toLowerCase();
        if (/[a-z]/i.test(c)) cntMap.set(c, (cntMap.get(c) || 0) + 1);
    }

    function complete(word) {
        let map = new Map(cntMap);
        for (let c of word) {
            c = c.toLowerCase();
            if (map.has(c)) map.set(c, map.get(c) - 1);
            if (map.get(c) === 0) map.delete(c);
        }
        return map.size === 0;
    }

    let result = null;
    for (let word of words) {
        if (result === null || word.length < result.length) {
            if (complete(word)) result = word;
        }
    }
    return result;
};
```
---
## [Minimum Absolute difference in BST](https://leetcode.com/problems/minimum-absolute-difference-in-bst/description/)
`一遍过` `BST` `inorder`

1. Array + sorted `O(nlgn)`
> min diff are two adj elemnts in the sorted array

2. BST + inorder
> Sorting via inorder traversal gives us sorted values, compare current one with previous one to reduce space complexity from O(n) to O(h).

```javascript
var getMinimumDifference = function(root) {
    let prev = null, minDiff = Infinity;
    (function inOrder(node) {
        if (!node) return;
        inOrder(node.left);
        if (prev) minDiff = Math.min(minDiff, Math.abs(node.val - prev.val));
        prev = node;
        inOrder(node.right);
    })(root);
    return minDiff;
};
```
---
## [Sentence Similarity](./hashtable.md#sentence-similarity)
