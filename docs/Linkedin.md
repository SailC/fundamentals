# Linkedin

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
## [House Robber](./dp.md#house-robber)
---
