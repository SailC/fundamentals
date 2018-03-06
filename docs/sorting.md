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
