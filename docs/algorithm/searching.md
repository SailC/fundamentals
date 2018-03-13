## [path sum II](https://leetcode.com/problems/path-sum-ii/description/)

`一遍过` `dfs`

```javascript
var pathSum = function(root, sum) {
    let results = [];
    function dfs(node, acc, path) {
        if (!node) return;
        if (!node.left && !node.right) {
            if (acc + node.val === sum) results.push([...path, node.val]);
            return;
        }
        path.push(node.val);
        dfs(node.left, acc + node.val, path);
        dfs(node.right, acc + node.val, path);
        path.pop();
    }
    dfs(root, 0, []);
    return results;
};
```
---
## [combination sum III](https://leetcode.com/problems/combination-sum-iii/description/)

`一遍过` `dfs`

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/216-ep100.png)

1. dfs
> Compared to `Combsum I&II` , this problem set a limit on the number of candidates per combination.
> since each number can be used only once and no dup in input numbers. we only need to update the position of the last added number.
> Time: C(9, k) = 9! / k ! / (9 - k)!
> Space: O(k + k * # of answers) 第一个k是递归深度，每个answer占空间 k.
2. bitmap
> Time: O(2 ^ 9) = (1 + 1) ^ 9  = C(9, 0) + C(9, 1) ... + C(9, 9)
> space: same as dfs

```javascript
var combinationSum3 = function(k, n) {
    let combs = [];
    function dfs(start, comb, acc) {
        if (acc >= n || comb.length >= k) {
            if (acc === n && comb.length === k) {
                combs.push([...comb]);
            }
            return;
        }
        for (let i = start; i <= 9; i++) {
            comb.push(i);
            dfs(i + 1, comb, acc + i);
            comb.pop();
        }
    }
    dfs(1, [], 0);
    return combs;
};

combinationSum3 = function(k, n) {
    let combs = [];
    for (let bitmap = 0; bitmap < (1 << 9); bitmap++) {
        let comb = [];
        let sum = 0;
        for (let j = 0; j < 9; j++) {
            if (bitmap & (1 << j)) {
                sum += j + 1;
                comb.push(j + 1);
            }
        }
        if (sum === n && comb.length === k)
            combs.push(comb);
    }
    return combs;
};
```
---
## [nested list weight sum](https://leetcode.com/problems/nested-list-weight-sum/description/)

1. dfs
> each nest level indicates 1 level deeper
> sum of current level = current integer val  * depth + sum of next level

```javascript
var depthSum = function(nestedList) {
    function dfs(list, depth) {
        let sum = 0;
        for (let nestInt of list) {
            if (nestInt.isInteger()) sum += depth * nestInt.getInteger();
            else sum += dfs(nestInt.getList(), depth + 1);
        }
        return sum;
    }
    return dfs(nestedList, 1);
};
```

---
## [nested list weight sum II](https://leetcode.com/problems/nested-list-weight-sum-ii/description/)

1. two pass (bottom up + topdown)
> calculate height first and use nested lsit weight sum i
2. one pass with accSum
> each upper level sum will appear in the next level , and we need to acc the sum of each level

```javascript
var depthSumInverse = function(nestedList) {
    let sum = 0, accSum = 0;
    let que = nestedList;

    while (que.length > 0) {
        let nextQue = [];
        for (let nestInt of que) {
            if (nestInt.isInteger()) {
                sum += nestInt.getInteger();
            } else {
                for (let x of nestInt.getList()) nextQue.push(x);
            }
        }
        que = nextQue;
        accSum += sum;
    }

    return accSum;
};

depthSumInverse = function(nestedList) {
    function getHeight(list) {
        let depth = 1;
        for (let nestInt of list) {
            if (!nestInt.isInteger()) {
                let d = getHeight(nestInt.getList());
                depth = Math.max(depth, 1 + d);
            }
        }
        return depth
    }

    function dfs(list, depth) {
        let sum = 0;
        for (let nestInt of list) {
            if (nestInt.isInteger()) sum += depth * nestInt.getInteger();
            else sum += dfs(nestInt.getList(), depth - 1);
        }
        return sum;
    }

    return dfs(nestedList, getHeight(nestedList));
};
```
