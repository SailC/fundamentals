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
