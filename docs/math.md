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
