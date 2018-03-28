## [top k frequent elements](https://leetcode.com/problems/top-k-frequent-elements/description/)

`有思路` `heap` `bucket sort`

1. sort
> Time: O(NlogN)
> space: O(n)
2. priority queue
maintain a max heap of size K to save k top most frequent element.
> Time: O(NlogK)
> space: O(K)
3. bucket sorting
> Time: O(N)
> Space: O(N) -> O(K)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/347-ep95.png)

```javascript
var topKFrequent = function(nums, k) {
    let n = nums.length;
    //build reverse index : cnt->num
    let cntMap = new Map();
    for (let num of nums) cntMap.set(num, (cntMap.get(num) || 0) + 1);
    let cnt2num = new Array(n + 1).fill(0).map(x => []);
    for (let [num, cnt] of cntMap) cnt2num[cnt].push(num);
    //get top k
    let topK = [];
    for (let cnt = n; cnt > 0; cnt--) {
        while (topK.length < k && cnt2num[cnt].length > 0) {
            topK.push(cnt2num[cnt].pop());
        }
        if (topK.length === k) break;
    }
    return topK;
};
```
---
## [top k frequent words](https://leetcode.com/problems/top-k-frequent-words/description/)

`有思路` `heap` `bucket sort`

1. sort
> Time : O(NlgN)
2. minHeap
> maintain a minHeap of k element, 以便每次踢出去的都是less frequent的货色，这样最好残留下来的就是topK.
> Time: O(NlgK)
3. bucket sort
> Time: O(NlgK)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/692-ep94.png)

```javascript
var topKFrequent = function(words, k) {
    let n = words.length;
    let cntMap = new Map();
    for (let word of words) cntMap.set(word, (cntMap.get(word) || 0) + 1);
    let cnt2word = new Array(n + 1).fill(0).map(x => new Heap((a, b) => a < b ? -1 : (a > b ? 1 : 0)));
    for (let [word, cnt] of cntMap) cnt2word[cnt].push(word);
    let topK = [];
    for (let cnt = n; cnt > 0 && topK.length < k; cnt--) {
        let words = cnt2word[cnt];
        while (words.size > 0 && topK.length < k) {
            topK.push(words.pop());
        }
    }
    return topK;
};

topKFrequent = function(words, k) {
    let n = words.length;
    let cntMap = new Map();
    for (let word of words) cntMap.set(word, (cntMap.get(word) || 0) + 1);
    let minHeap = new Heap((a, b) => {
        let cntA = cntMap.get(a), cntB = cntMap.get(b);
        if (cntA < cntB) return -1;
        if (cntA > cntB) return 1;
        return a > b ? -1: 1;
    });
    for (let word of cntMap.keys()) {
        minHeap.push(word);
        if (minHeap.size > k) minHeap.pop();
    }

    let topK = [];
    while (minHeap.size > 0) topK.push(minHeap.pop());
    return topK.reverse();
};
```
---
## [h index](https://leetcode.com/problems/h-index/description/)

1. Comparison Sort

> it's pretty hard to understand the definition of the H-index:

> A scientist has index h if h of his/her N papers have at least h citations each, and the other N − h papers have no more than h citations each

> The second half of the definition seems useless but it's not. We can easily find h = 1, which means 1 of his paper has at least 1 citation, but the second half enforce the rest of his paper as at most 1 citation, which means this author really sucks.

> As illustrated in the solution https://leetcode.com/problems/h-index/solution/ .
> H-index is the last paper that has citations greater than or equal to the total number of paper so far (scanning left to right).

> Since the paper is sorted in decending order, if the `h-th` paper has citations more than h, then the previous papers all have citations more than h, (which means there are at h papers that have citations more than h, we satisfy the first half of the definition).

> Why is H-index the last paper that has citations >= h ? because the rest of the paper `N - h` has citation <= h . If we did not pick the last paper, then there might be paper from `[h + 1, N]` that has citation > h.

2. Counting sort

> in our problem, the keys are the citations of each paper which can be much larger than the number of papers nn. It seems that we cannot use counting sort. The trick here is the following observation:

> Any citation larger than N can be replaced by N and the h-index will not change after the replacement

```javascript
var hIndex = function(citations) {
    let n = citations.length;
    // comparison sort descending order
    citations.sort((a, b) => b - a);
    // find hIndex
    let hIndex = 0;
    for (let i = 0; i < n; i++) {
		// num of papers so far = i + 1
        if (citations[i] >= i + 1) hIndex = i + 1;
    }

    return hIndex;
};

var hIndex = function(citations) {
    let n = citations.length;
    let cnts = countCitations(citations);
    let hCnt = 0;
    for (let h = n; h >= 0; h--) {
        hCnt += cnts[h];
				// hCnt === # of paper with citation >= h
        // 剩下的 paper citation 都 < h
        if (hCnt >= h) return h;
    }
    return 0;
};

function countCitations(citations) {
    let n = citations.length;
    let counter = new Array(n + 1).fill(0);

        // counting # of papers for each citation number
    for (let cite of citations) {
        counter[Math.min(n, cite)]++;
    }
    return counter;
}
```
---
## [h index II](https://leetcode.com/problems/h-index-ii/description/)

1. Binary Search
> Use binary search to find the smallest idx i, so that `citation[i] >= n - i` . `[0: i)` has `i` papers, `[i: n)` has `n - i` papers.
> 可以把 `n - mid` 理解为可能的hIndex，hIndex尽可能大意味着i要尽可能小
>  如果`citation[mid] < n - mid` 那么右边paper的citation即使全部大于 `n - mid` 也凑不齐 `n - mid` 篇paper。所以这个时候只能认怂，右移i，减小hindex。
>  如果 `citation[mid] === n - mid` 那么显然符合hIndex定义
>  如果 `citation[mid] > n - mid` 那么 它有可能是hIndex，当前面的paper都比较烂的时候，他也有可能不是hIndex，当前面的paper水平稍微次一点的时候。不管如何都应该保留其作为候选
>  随意目标是选出第一个 满足 `citation[mid] >= n - mid` 的mid， `n - mid`就是其index . 如果不存在，则hIndex为0

```javascript
var hIndex = function(citations) {
    let n = citations.length;
    let lo = 0, hi = n - 1;
    while (lo < hi) {
        let mid = lo + ~~((hi - lo) / 2);
        if (citations[mid] >= n - mid) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    //bug1: return n - lo;
    return citations[lo] >= n - lo ? n - lo : 0;
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

## [meeting room](https://leetcode.com/problems/meeting-rooms/description/)

```
if there is an overlapp in the meeting time, then a person can't attend all meetings.
```

```javascript
var canAttendMeetings = function(intervals) {
    intervals.sort((interval1, interval2) => interval1.start - interval2.start);
    for (let i = 0; i < intervals.length; i++) {
        if (i > 0 && intervals[i].start < intervals[i - 1].end) return false;
    }
    return true;
};
```

---

## [meeting room II](https://leetcode.com/problems/meeting-rooms-ii/description/)

```
when do we increase the meeting room, when the new meeting starts before the next existing meeting ends.

if the new meeting starts after the old meeting ends, then the new meeting can use the old room.

`minHeap` O(nlgn)
we can use a minHeap to store all the existing meetings (tracking the minimum end of the meetings).
for each new meeting, check the minHeap to see if the earlest ending meeting will end before it begins, if not , we need a new room (put the new meeting in heap). If so, we can share the same room, merge the intervals by updating the end time and put it back to the heap.

`greedy`
we sort the starting and ending time respectively as we only care about the number of onging meetings at any given point.
```

![](https://static.notion-static.com/79c61c4e43d94cbd9190b46285d6a84c/Scannable_Document_2_on_Dec_9_2017_at_10_52_01_AM.png)

```javascript
var minMeetingRooms = function(intervals) {
    let starts = intervals.map(x => x.start).sort((a, b) => a - b);
    let ends = intervals.map(x => x.end).sort((a, b) => a - b);
    let j = 0; //next meeting to finish
    let minRooms = 0;
    for (let start of starts) {
        let nextEnd = ends[j];
        if (start < nextEnd) minRooms++;
        else j++;
    }
    return minRooms;
};

minMeetingRooms = function(intervals) {
    intervals.sort((a, b) => a.start - b.start);
    let heap = new Heap((a, b) => a.end - b.end);
    for (let interval of intervals) {
        if (heap.size === 0) {
            heap.push(interval);
        } else {
            let nextEnd = heap.pop();
            if (interval.start >= nextEnd.end) {
                nextEnd.end = interval.end;
            } else {
                heap.push(interval);
            }
            heap.push(nextEnd);
        }
    }
    return heap.size;
};
```

---

## [best meeting point](https://leetcode.com/problems/best-meeting-point/description/)

```
这道题根本猜不透啊
怎么也想不到x坐标和y坐标这两个子问题是独立的

曼哈顿距离 (p1, p2) = |p2.x - p1.x| + |p2.y - p1.y|

可以分别求解x坐标的最优解和y坐标的最优解
然后得到的最优x，y就是出发点

求一维问题的时候可以记录下所有home的位置，sort一下，选middle home，这样在它的左右两边都有同样数量的home，比较省力，不用走非home的节点。

这题是是一维上的best meeting point。 答案是median。需要证明。形式上对应lasso regularization

https://math.stackexchange.com/a/113386 证明
```

```javascript
var minTotalDistance = function(grid) {
    let rows = [], cols = []; //save indexes of homes
    let m = grid.length;
    if (m === 0) return 0;
    let n = grid[0].length;
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === 1) {
                rows.push(i);
                cols.push(j);
            }
        }
    }
    cols.sort((a, b) => a - b);
    return minDistSum(rows) + minDistSum(cols);
}

function minDistSum(points) {
    let target = points[~~(points.length / 2)];
    return points.reduce((acc, cur) => acc + Math.abs(cur - target), 0);
}
```

---

## [median of two sorted array](https://leetcode.com/problems/median-of-two-sorted-arrays/description/)

```
二分搜索，每次chop off k / 2个元素 hopefully

用递归实现二分搜索，有特殊case
step1: make sure num1.length <= num2.length
step2: make sure num1.length > 0
step3: make sure k > 1

这样可以简化之后的二分
因为之后的二分保证了 0 < num1.length <= num2.length && k > 1

k > 1 保证了 k / 2 >= 1 也就是num1 至少划分出一个元素
```

```javascript
var findMedianSortedArrays = function(nums1, nums2) {
    let n = nums1.length + nums2.length;
    if (n % 2 === 0) return (findKth(nums1, nums2, ~~(n / 2)) + findKth(nums1, nums2, ~~(n / 2) + 1)) / 2;
    return findKth(nums1, nums2, ~~(n / 2) + 1);
};

const findKth = (nums1, nums2, k) => {
    if (nums1.length > nums2.length) return findKth(nums2, nums1, k);
    if (nums1.length === 0) return nums2[k - 1];
    // 0 < nums1.length <= nums2.length
    if (k === 1) return Math.min(nums1[0], nums2[0]);
    let m = Math.min(nums1.length, ~~(k / 2));
    let n = k - m;
    if (nums1[m - 1] === nums2[n - 1]) return nums1[m - 1];
    if (nums1[m - 1] < nums2[n - 1]) return findKth(nums1.slice(m), nums2, k - m);
    return findKth(nums1, nums2.slice(n), k - n);
};
```

---

## [non overlapping intervals](https://leetcode.com/problems/non-overlapping-intervals/description/)

sort the intervals ending position increasing
maintain a que of non-overlapped intervals
if overlapped , pick the upcomming interval to remove as it's more likely to overlapped with previous intervals and upcomming intervals

```javascript
var eraseOverlapIntervals = function(intervals) {
    let nonOverlap = [];
    intervals.sort((a, b) => a.end - b.end);
    for (let interval of intervals) {
        if (nonOverlap.length === 0 || nonOverlap[nonOverlap.length - 1].end <= interval.start) {
            nonOverlap.push(interval);
        }
    }
    return intervals.length - nonOverlap.length;
};
```

---

为什么要按照 start sort? 因为这样 只需要考虑 upcomming.start 和 last.end 之间的关系，而不用对之前 interval 逐一判断overlap. O(n ^ 2) => O(nlgn)

为什么按照 end sort. 一般考虑到 较大的upcoming.end 会和 future intervals overlap的个数较多，所以通常和greedy结合起来。戳气球，和Non-overlapping intervals 都是
如果不按end sort，那么先入栈的interval有可能是end比较大的，一个interval就可以在那儿占着茅坑不拉屎不让其他conflicting interval进来。

关于 interval的二分搜索比较蛋疼，可以用bst或者sorted array来存储intervals

---
