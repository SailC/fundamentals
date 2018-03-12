##[Sqrt(x)](https://leetcode.com/problems/sqrtx/description/)
[perm link](./Google.md#sqrtx)

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
