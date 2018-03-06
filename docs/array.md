## [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/description/)

`一遍过` `prefixsum`

0. bruteforce O(n^2)
> for each index, use O(n) to compute on the fly the leftSum & rightSum and see if they're equal

1. prefix sum (preprocessing) + array O(n)
> We need to quickly compute the sum of values to the left and the right of every index.
> Let's say we knew S as the sum of the numbers, and we are at index i. If we knew the sum of numbers leftsum that are to the left of index i, then the other sum to the right of the index would just be S - nums[i] - leftsum
> trade space for time

2. prefix on the fly
> use only a variable to represent prefixSum and commpute the suffixSum on the fly in O(1).
> O(1) space

```javascript
var pivotIndex = function(nums) {
    let n = nums.length;
    let left = new Array(n).fill(0), right = new Array(n).fill(0);
    let sumLeft = 0, sumRight = 0;
    for (let i = 0; i < n; i++) {
        [left[i], sumLeft] = [sumLeft, sumLeft + nums[i]];
        [right[n - 1 - i], sumRight] = [sumRight, sumRight + nums[n - 1 - i]];
    }
    for (let i = 0; i < n; i++) {
        if (left[i] === right[i]) return i;
    }
    return -1;
};

pivotIndex = function(nums) {
    let n = nums.length;
    let sum = nums.reduce((x, accSum) => x + accSum, 0);
    let prefixSum = 0;
    for (let i = 0; i < n; i++) {
        if (prefixSum === sum - nums[i] - prefixSum) return i;
        prefixSum += nums[i];
    }
    return -1;
};
```
---
## [Majority Element](https://leetcode.com/problems/majority-element/description/)

`hashmap` `sorting` `voting` `quick-select` `divide&conquery`

1. brute force O(n^2)
> iterates over the array, and then iterates again for each number to count its occurrences. As soon as a number is found to have appeared more than any other can possibly have appeared, return it.
2. hashmap O(n)
> We can use a HashMap that maps elements to counts in order to count occurrences in linear time by looping over nums. Then, we simply return the key with maximum value.
3. sorting O(nlgn)
If the elements are sorted in monotonically increasing (or decreasing) order, the majority element can be found at index `n/2` or `n/2 + 1` if even
4. divide & conqure O(nlogn)
> base case; the only element in an array of size 1 is the majority
> recurse on left and right halves of this slice.
> if the two halves agree on the majority element, return it.
> otherwise, count each element and return the "winner". O(n)
5. bit vote O(32 * n)
> 对每一位计算该bit的majority，也就是最后答案的bit
6. Boyer-Moore vote O(n)
> 每个数都check一下目前的candidate是不是自己，是的话投一票，不是的话减一，如果majority存在的话，投票的最后结果一定是majority.
7. quick select O(n)
> 求第 `n / 2` th number in the sorted array.

```javascript
var majorityElement = function(nums) {
    nums.sort((a, b) => a - b);
    let n = nums.length;
    return nums[~~(n / 2)];
};

majorityElement = function(nums) {
    let n = nums.length;
    let cntMap = new Map();
    for (let num of nums) cntMap.set(num, (cntMap.get(num) || 0) + 1);
    for (let num of cntMap.keys()) {
        if (cntMap.get(num) > ~~(n / 2)) return num;
    }
};

majorityElement = function(nums) {
    let vote = 0, candidate = 0;
    for (let num of nums) {
        if (vote === 0) candidate = num;
        if (num === candidate) vote++;
        else vote--;
    }
    return candidate;
};

majorityElement = function(nums) {
    let n = nums.length;
    let majority = 0;
    for (let i = 0; i < 32; i++) {
        let mask = 1 << i;
        let count = 0;
        for (let num of nums) {
            if (num & mask) count++;
        }
        if (count > ~~(n / 2)) majority |= mask;
    }
    return majority;
};
```

---
## [partition label](https://leetcode.com/problems/partition-labels/description/)

`一遍过` `回味` `partition` `greedy` `hashtable`

1. bruteforce
> Let's try to repeatedly choose the smallest left-justified partition
> For each letter encountered, process the last occurrence of that letter, extending the current partition [anchor, i] appropriately.
> invariant: `[anchor, i]` justified partition : each letter only appears in this partition
> for each char, use `O(n)` to find the last index of it.
2. hashtable
> use hashtable to preprocess the lastIndex info

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/763-ep161.png)

```javascript
var partitionLabels = function(S) {
    let indexMap = new Map();
    let n = S.length;
    for (let i = 0; i < n; i++) indexMap.set(S[i], i);
    let ans = [], max = 0, lastIdx = -1;
    for (let i = 0; i < n; i++) {
        let c = S[i];
        max = Math.max(max, indexMap.get(c));
        if (max === i) {
            ans.push(i - lastIdx);
            lastIdx = i;
        }
    }
    return ans;
};
```
---

## [Max chunks to make sorted](https://leetcode.com/problems/max-chunks-to-make-sorted/description/)
`无思路` `partition` `greedy`

1. left max & min right
> Iterate through the array, each time all elements to the left are smaller (or equal) to all elements to the right, there is a new chunk.

2. max so far
> keep track of the max value so far, if the current index equals the max value so far, increase the # of chunk by one.

```javascript
var maxChunksToSorted = function(arr) {
    let ans = 0, max = 0, n = arr.length;
    for (let i = 0; i < n; i++) {
        max = Math.max(max, arr[i]);
        if (max === i) ans++;
    }
    return ans;
};

maxChunksToSorted = function(arr) {
    let n = arr.length;
    let left = new Array(n), right = new Array(n);
    for (let i = 0; i < n; i++) {
        left[i] = i === 0 ? arr[i] : Math.max(left[i - 1], arr[i]);
    }
    for (let i = n - 1; i >= 0; i--) {
        right[i] = i === n - 1 ? arr[i] : Math.min(right[i + 1], arr[i]);
    }
    let ans = 1;
    for (let i = 0; i < n - 1; i++) {
        if (left[i] < right[i + 1]) ans++;
    }
    return ans;
};
```

---

## [Max chunks to make sorted II](https://leetcode.com/problems/max-chunks-to-make-sorted-ii/description/)

1. Mapping + reduce  O(nlgn)
> 将这题转换为 ver1.
> arr = [2, 3, 5, 4, 4]
> sorted = [2, 3, 4, 4, 5]
> indices = [0, 1, 4, 2, 3]
2. map + list + maxSofar O(nlgn)
> 在ver1 的基础上将indexMap拓展，value是index的list。这样每次extend window的时候就知道当前window的末尾index。
3. leftMax + rightMin O(n)
4. zip + cntMap O(nlgn)
> 原始数组和排序之后的数组在当前window出现的字符的个数相当才能切割.

`有思路` `不熟练` `greedy` `partition` `hashmap` `sort` `prefixsum`

```javascript
var maxChunksToSorted = function(arr) {
    let n = arr.length;
    let indexMap = new Map();
    let sorted = [...arr].sort((a, b) => a - b);
    for (let i = 0; i < n; i++) {
        if (!indexMap.has(sorted[i])) indexMap.set(sorted[i], []);
        indexMap.get(sorted[i]).push(i);
    }
    let max = 0, cnt = 0;
    for (let i = 0; i < n; i++) {
        let idx = indexMap.get(arr[i]).shift();
        max = Math.max(max, idx);
        if (i === max) cnt++;
    }
    return cnt;
};

maxChunksToSorted = function(arr) {
     let n = arr.length;
     let leftMax = new Array(n), rightMin = new Array(n);
     for (let i = 0; i < n; i++) {
         leftMax[i] = i === 0 ? arr[i] : Math.max(leftMax[i - 1], arr[i]);
     }
     for (let i = n - 1; i >= 0; i--) {
         rightMin[i] = i === n - 1 ? arr[i] : Math.min(rightMin[i + 1], arr[i]);
     }
     let cnt = 1;
     for (let i = 0; i < n - 1; i++) {
         if (leftMax[i] <= rightMin[i + 1]) cnt++;
     }
     return cnt;
 };

maxChunksToSorted = function(arr) {
    let n = arr.length;
    let sorted = [...arr].sort((a, b) => a - b);
    const zip = (a, b) => a.map((x, i) => [x, b[i]]);
    let cntMap = new Map();

    let cnt = 0;
    let diff = 0;
    for (let [x, y] of zip(arr, sorted)) {
        cntMap.set(x, (cntMap.get(x) || 0) + 1);
        if (cntMap.get(x) === 0) diff--;
        if (cntMap.get(x) === 1) diff++;

        cntMap.set(y, (cntMap.get(y) || 0) - 1);
        if (cntMap.get(y) === 0) diff--;
        if (cntMap.get(y) === -1) diff++;

        if (diff === 0) cnt++;
    }
    return cnt;
};
```
