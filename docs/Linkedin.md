## [Valid Perfect Square](https://leetcode.com/problems/valid-perfect-square/description/)

`一遍过` `binary search`

1. bruteforce O(n)
> `for (let x = 1; x ^ 2 <= n; x++) if (x ^ 2 === num) return true;`
2. binary search O(lgn)
> f(x) = x ^ 2 <= n
> true, true, true, ..., true, false, false,...
> find the last true and check if it's the factor.

```javascript
var isPerfectSquare = function(num) {
    let lo = 1, hi = num;
    while (lo < hi) {
        let mid = lo + ~~((hi - lo + 1) / 2);
        if (mid * mid > num) hi = mid - 1;
        else lo = mid;
    }
    return lo * lo === num;
};
```
---
## [House Robber](https://leetcode.com/problems/house-robber/description/)
`一遍过` `回味` `dp`

1. bruteforce
for each house , decide whether to rob it or not. `2^n` combination of choices.
2. recursion + mem
3. dp with robNorob space O(1)
> rob[i] max money after robbing house i , noRob[i] max money after not robbing house i
4. dp with maxRob(ornot) space O(n)
> dp[i] mx money after robbing / not robbing house i
5. dp with maxRob(ornot) space O(1)

```javascript
var rob = function(nums) {
    let n = nums.length;
    let cache = new Array(n).fill(-1);
    function robFrom(i) {
        if (i >= n) return 0;
        if (cache[i] !== -1) return cache[i];
        cache[i] = Math.max(nums[i] + robFrom(i + 2), robFrom(i + 1));
        return cache[i];
    }
    return robFrom(0);
};

rob = function(nums) {
    let rob = 0, noRob = 0;
    for (let num of nums) {
        [rob, noRob] = [noRob + num, Math.max(rob, noRob)];
    }
    return Math.max(rob, noRob);
};

rob = function(nums) {
    let n = nums.length;
    // max money after visiting house[i]
    let dp = new Array(n + 1).fill(0);
    dp[1] = nums[0];
    for (let i = 2; i <= n; i++) {
        dp[i] = Math.max(nums[i - 1] + dp[i - 2], dp[i - 1]);
    }
    return dp[n];
};

rob = function(nums) {
    let n = nums.length;
    // max money after visiting house[i]
    let f2 = 0, f1 = 0;
    for (let i = 0; i < n; i++) {
        [f1, f2] = [Math.max(nums[i] + f2, f1), f1];
    }
    return f1;
};
```
