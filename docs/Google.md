# Sorting & Searching
## [Sqrt(x)](https://leetcode.com/problems/sqrtx/description/)
`有思路` `一遍过`

1. brute force
> for i in [0, x], find the last i so that `i ^ 2 <= x`.
2. binary search
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
