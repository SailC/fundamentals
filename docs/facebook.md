##[Sqrt(x)](https://leetcode.com/problems/sqrtx/description/)
[perm link](./Google.md#sqrtx)

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

## [Two Sum in BST](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/description/)
`一遍过` `双指针靠拢` `BST`

1. `hashset + tree traversal (bfs/dfs)`
> O(n) space + O(n) time

2. `in order traversal -> array + two pointers`
> O(n) space + O(n) time

```javascript
var findTarget = function(root, k) {
    let arr = [];
    (function inOrder(node) {
        if (!node) return;
        inOrder(node.left);
        arr.push(node.val);
        inOrder(node.right);
    })(root);
    let lo = 0, hi = arr.length - 1;
    while (lo < hi) {
        if (arr[lo] + arr[hi] === k) return true;
        if (arr[lo] + arr[hi] < k) lo++;
        else hi--;
    }
    return false;
};

findTarget = function(root, k) {
    let set = new Set();
    function dfs(node) {
        if (!node) return false;
        if (set.has(k - node.val)) return true;
        set.add(node.val);
        return dfs(node.left) || dfs(node.right);
    }
    return dfs(root);
};

findTarget = function(root, k) {
    let set = new Set();
    function bfs(node) {
        let que = root ? [root] : [];
        while (que.length > 0) {
            let node = que.shift();
            if (set.has(k - node.val)) return true;
            set.add(node.val);
            if (node.left) que.push(node.left);
            if (node.right) que.push(node.right);
        }
        return false;
    }
    return bfs(root);
};
```
---
## [Best Time to Buy and Sell Stock](./dp.md#best-time-to-buy-and-sell-stock)
---
## [Number of Islands](./dfs.md#number-of-islands)
---
## [Partition to K equal Sum subset](./dp.md#partition-to-k-equal-sum-subset)
