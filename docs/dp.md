## [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/description/)

1. divide & conquer
> `O(n)`uan
2. dp
> `dp[i] = Math.max(dp[i - 1] + nums[i - 1], nums[i - 1]);`

```javascript
var maxSubArray = function(nums) {
    let n = nums.length;
    //let dp = new Array(n + 1).fill(0);
    let curMax = 0;
    let maxVal = -Infinity;
    for (let i = 1; i <= n; i++) {
        //dp[i] = Math.max(dp[i - 1] + nums[i - 1], nums[i - 1]);
        curMax = Math.max(curMax + nums[i - 1], nums[i - 1]);
        // maxVal = Math.max(maxVal, dp[i]);
        maxVal = Math.max(maxVal, curMax);
    }
    return maxVal;
};

maxSubArray = function(nums) {
    let n = nums.length;

    function maxSub(lo, hi) {
        if (lo > hi) return -Infinity;
        let mid = lo + ~~((hi - lo) / 2);
        let maxSum = nums[mid];
        let sum = nums[mid];
        for (let i = mid - 1; i >= 0; i--) {
            sum += nums[i];
            maxSum = Math.max(maxSum, sum);
        }
        sum = maxSum;
        for (let i = mid + 1; i < n; i++) {
            sum += nums[i];
            maxSum = Math.max(maxSum, sum);
        }
        return Math.max(maxSum, maxSub(lo, mid - 1), maxSub(mid + 1, hi));
    }

    return maxSub(0, n - 1);
};
```
---
