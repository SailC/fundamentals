## [self deviding numbers](https://leetcode.com/problems/self-dividing-numbers/description/)

`一遍过` `从低位开始分解一串数字`

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/728-ep111-1.png)
```javascript
var selfDividingNumbers = function(left, right) {
    let result = [];

    function selfDividing(num) {
        let x = num;
        while (num > 0) {
            let digit = num % 10;
            if (digit === 0 || x % digit !== 0) return false;
            num = ~~(num / 10); //注意不要直接除
        }
        return true;
    }

    for (let num = left; num <= right; num++) {
        if (selfDividing(num)) result.push(num);
    }
    return result;
};
```
---
## [pow(x,n)](https://leetcode.com/problems/powx-n/description/)

1. `divide & conquer`
> edge case1: `n < 0`
> edge case2: `n === 0`
> save `myPow(x, n / 2)` to reduce time complexity.

```javascript
var myPow = function(x, n) {
    if (n < 0) return 1 / myPow(x, -n);
    if (n === 0) return 1;
    if (x === 0) return 0;
    let half = myPow(x, ~~(n / 2));
    return n % 2 === 0 ? half * half : half * half * x;
};
```

---

## [sum of square numbers](https://leetcode.com/problems/sum-of-square-numbers/description/)

```javascript
var judgeSquareSum = function(c) {
    for (let i = 0; i * i <= c; i++) {
        let j = Math.sqrt(c - i * i);
        if (j === ~~(j)) return true;
    }
    return false;
};
```
