# Bit operation

## [Prime Number of Set Bits in Binary Representation](https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/description/)

`一遍过` `prime number` `bit opr`

1. 按照题意
>对 `[L,R]`之间的每个数计算set bit， 如果这个cnt是prime那么结果加1.
>prime计算的时候可以优化到`sqrt(x)`
>set bit 计算的时候也可以优化
> 最大值 `10^6`， 也就是 `2 ^ 20`, 20位bit 中的prime bit总共就 {2, 3, 5, 7, 11, 13, 17, 19} 可以把他们放在set或者array或者binary mask里面，避免每次都计算
>Time: O(R-L)
>Space: O(1)

![3](./images/3.png)

```javascript
var countPrimeSetBits = function(L, R) {
    const isPrime = x => {
        //for (let i = 2; i < x; i++) {
        for (let i = 2; i <= Math.sqrt(x); i++) {
            if (x % i === 0) return false;
        }
        return x > 1;
    };
    const countSet = x => {
        let cnt = 0;
        // for (let i = 0; i < 32; i++) cnt += (x >>> i) & 1;
        for (; x > 0; x >>>= 1) cnt += x & 1;
        return cnt;
    }
    let arr = [];
    for (let x = L; x <= R; x++) arr.push(x);
    return arr.map(countSet).filter(isPrime).length;
};
```
---
## [hamming distance](https://leetcode.com/problems/hamming-distance/description/)

> xor + check each set bit (if diff, bit is set to 1)
> `n & (n - 1)` clear the last set bit (===1)
> `n & -n` get the lowest set bit (BIT tree)

```javascript
var hammingDistance = function(x, y) {
    let xor = x ^ y;
    let dist = 0;
    for (let i = 0; i < 32; i++) {
        dist += (xor >> i) & 1;
    }
    return dist;
};

// n & (n – 1) will clear the last significant bit of n , e.g. n = 4 = 100 -> 100 ^ 011 = 000
var hammingDistance = function(x, y) {
    var num = x ^ y;
    var distance = 0;
    while (num !== 0) {
        num &= (num - 1);
        distance += 1;
    }
    return distance;
}
```
---
## [total hamming distance](https://leetcode.com/problems/total-hamming-distance/description/)

> count zeros and ones for each bit
> scan each bit (total 32 bits) , for each bit , the total hamming distance is the number of ones * the number of zeros
> the distance is between 1 and 0 , each one can map to each zero to form a distance.

```javascript
var totalHammingDistance = function(nums) {
    let dist = 0;
    for (let i = 0; i < 32; i++) {
        let ones = 0;
        for (let num of nums) ones += (num >> i) & 1;
        let zeros = nums.length - ones;
        dist += ones * zeros;
    }
    return dist;
};
```
---
## [divide two integers](https://leetcode.com/problems/divide-two-integers/description/)

整数除法的实现可以转化成位移操作，
```
17 / 3 = 5 <=
17 = 3 * 5
    = 3 * (1 << 2 + 1 << 1)
ans = (1 << 2 + 1 << 1)
```

```javascript
var divide = function(dividend, divisor) {
    const MAX_INT = ((1 << 31) >>> 0) - 1;
    const MIN_INT = 1 << 31;
    if (dividend === 0) return 0;
    if (divisor === 0 ) return MAX_INT;
    if (dividend === MIN_INT) {
        if (divisor === -1) return MAX_INT;
        if (divisor === 1) return MIN_INT;
    }

    let sign = (dividend > 0 && divisor > 0) || (dividend < 0 && divisor < 0) ? 1 : -1;
    [divisor, dividend] = [divisor, dividend].map(Math.abs);

    let quot = 0;
    // while (dividend >= divisor) {
    //     let i = 1, j = divisor;
    //     while (j + j <= dividend) {
    //         j += j;
    //         i += i;
    //     }
    //     quot += i;
    //     dividend -= j;
    // }

    while (dividend >= divisor) {
        let shift = 0;
        while ( (divisor << shift) <= dividend) shift++;
        quot += 1 << (shift - 1);
        dividend -= divisor << (shift - 1);
    }

    return sign * quot;
};
```
---
##[Number Complement](https://leetcode.com/problems/number-complement/description/)

`无思路` `xor`

1. bit opr 正向思考
> 考察用 xor来保存或者取反.
> bit mask `11100000` 可用来进行xor来达到将前3位bit取反，后5位保留的目的
> 本题的目的是 求`0000101`的特殊complement, 要求将前面的0保留，将后面的取反
> 所以我们的目的是构建一个mask `0000111`。
> `while (mask < num) mask = (mask << 1) | 1;`
2. bit opr 逆向思考
> 先将 num 取反 `0000101 => 1111010`
> 然后我们的目的是保留后三位，取反前面的bit
> 所以我们要构建一个 `1111000`的mask罩上去
> `int mask = ~0;        `
> `while (num & mask) mask <<= 1;`

```javascript
var findComplement = function(num) {
    let comp = 0;
    for (let i = 0; num > 0; i++, num >>>= 1) {
        comp += (1 ^ (num & 1)) << i
    }
    return comp;
};

findComplement = function(num) {
    let mask = 0;
    while (mask < num) mask = (mask << 1) | 1;
    return mask ^ num;
};

findComplement = function(num) {
    let mask = ~0;
    while (mask & num) mask <<= 1;
    return mask ^ ~num;
};
```
---

## [missing number](https://leetcode.com/problems/missing-number/description/)

> The basic idea is to use XOR operation. We all know that a^b^b =a, which means two xor operations with the same number will eliminate the number and reveal the original number.
> In this solution, I apply XOR operation to both the index and value of the array. In a complete array with no missing numbers, the index and value should be perfectly corresponding( nums[index] = index), so in a missing array, what left finally is the missing number.

```javascript
var missingNumber = function(nums) {
    let missing = 0;
    for (let i = 0; i < nums.length; i++) {
        missing ^= (i ^ nums[i])
    }
    return missing ^ nums.length;
};
```
