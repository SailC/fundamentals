# sliding window

## [minimum window substring](https://leetcode.com/problems/minimum-window-substring/description/)

> `two pointer + cntMap`
use two pointer to form a window and use cntMap to save the count of each character within the window.
try to extend the end of the window by iterating through `j` .
> `how to check if the rule is satisfied`
O(1) time instead of iterating through the cntMap.
use `cnt` to indicates how many kinds of char has not been included.
`cnt === 0` means the window includes all kinds of chars in `t` with at least the same number of appearances.

```javascript
var minWindow = function(s, t) {
    let result = '';
    let cntMap = new Map();
    for (let c of t) cntMap.set(c, (cntMap.get(c) || 0) + 1);
    let cnt = cntMap.size;
    let i = 0; // start pointer of the window;
    for (let j = 0; j < s.length; j++) {
        let c = s[j];
        if (cntMap.has(c)) {
            cntMap.set(c, cntMap.get(c) - 1);
            if (cntMap.get(c) === 0) cnt--;
        }

        while (cnt === 0) {
            let window = s.slice(i, j + 1);
            if (result === '' || window.length < result.length) {
                result = window;
            }
            let c = s[i];
            if (cntMap.has(c)) {
                cntMap.set(c, cntMap.get(c) + 1);
                if (cntMap.get(c) === 1) cnt++;
            }
            i++;
        }
    }
    return result;
};
```

---

## [smallest range](https://leetcode.com/problems/smallest-range/description/)

> 思路和min window substring一样
cntMap 表示每一个list出现的num次数，window rule :
对于每一列i, cntMap[i] <= 0. (cntMap表示除了window里的num之外，还需要多少个该列的元素)
> 先找出最大和最小值，然后行成一个boundary，然后不断移动头尾指针缩小range,同时更新cntMap和cnt

```javascript
var smallestRange = function(nums) {
    let indexMap = new Map(), max = -Infinity, min = Infinity;
    let n = nums.length;
    for (let i = 0; i < n; i++) {
        for (let num of nums[i]) {
            [min, max] = [Math.min(min, num), Math.max(max, num)];
            if (!indexMap.has(num)) indexMap.set(num, new Set());
            indexMap.get(num).add(i);
        }
    }

    let start = null, end = null;

    let cntMap = new Array(n).fill(1), cnt = n;
    let i = min;
    for (let j = min; j <= max; j++) {
        if (indexMap.has(j)) {
            for (let idx of indexMap.get(j)) {
                cntMap[idx]--;
                if (cntMap[idx] === 0) cnt--;
            }
        }

        while (cnt === 0) {
            if (start === null || j - i < end - start || i < start) {
                [start, end] = [i, j];    
            }
            if (indexMap.has(i)) {
                for (let idx of indexMap.get(i)) {
                    cntMap[idx]++;
                    if (cntMap[idx] === 1) cnt++;
                }
            }
            i++;
        }

    }

    return [start, end];
};
```
---

## [minimum size subarray sum](https://leetcode.com/problems/minimum-size-subarray-sum/description/)

> 直觉只能想到 暴力解法 O(n^2) 找出所有可能的subarray， 然后取sum >= s的长度最小的那个
 看到提示发现其实two pointer是个好办法， 因为subarray 只从 whole array trop后得到的
简化版 minimum window substring.
check rule -> `sum >= s`

> O(nlgn) 的做法比较不好想，用runningSum实现。
求segment total starting from index i -> find accSum[i] + target, in [i: n).
use binary search.

```javascript
var minSubArrayLen = function(s, nums) {
    let minLen = 0, i = 0, curSum = 0;
    for (let j = 0; j < nums.length; j++) {
        curSum += nums[j];
        while (curSum >= s) {
            minLen = minLen === 0 ? j - i + 1 : Math.min(minLen, j - i + 1);
            curSum -= nums[i];
            i++;
        }
    }
    return minLen;
};

minSubArrayLen = function(s, nums) {
    let minLen = 0, n = nums.length;
    let accSum = new Array(n + 1).fill(0);
    for (let i = 1; i <= n; i++) accSum[i] = nums[i - 1] + accSum[i - 1];
    for (let i = 1; i <= n; i++) {
        let end = binSearch(accSum, i, n, accSum[i - 1] + s);
        if (end > n) continue;
        if (minLen === 0 || end - i + 1 < minLen) minLen = end - i + 1;
    }
    return minLen;
}

function binSearch(accSum, lo, hi, target) {
    while (lo < hi) {
        let mid = lo + ~~((hi - lo) / 2);
        if (accSum[mid] >= target) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return (accSum[lo] >= target) ? lo : lo + 1;
}
```

---

## [repeated dna sequence](https://leetcode.com/problems/repeated-dna-sequences/description/)

```javascript
var findRepeatedDnaSequences = function(s) {
    let repeated = new Set();
    let result = new Set();
    let i = 0; //start of the window
    for (let j = 9; j < s.length; j++) {//end of the window
        let window = s.slice(i, j + 1);
        if (repeated.has(window)) {
            result.add(window);
        } else {
            repeated.add(window);
        }
        i++;
    }
    return [...result];
};
```
