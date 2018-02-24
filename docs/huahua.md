# huahua jiang

## [Letter Case Permutation](https://leetcode.com/problems/letter-case-permutation/description/)
`有思路` `dfs` `bfs`

```
Note:
S will be a string with length at most 12.
input size较小，推测时间复杂度 `2 ^ n` or `n!`
```

1. dfs
> dfs 空间复杂度较小，因为只需要存储当前解的空间
branch factor = 2
时间复杂度 `O(n * 2 ^ l)` l is the # of letters. A total of `2 ^ l` new string and for string takes `O(n)` time to construct
Space complexity `O(n) === stack depth` + `O(n * 2 ^ l) === solution array`.

2. bfs
> bfs 要存储所有partial solution.
> bfs max level === n

```javascript
var letterCasePermutation = function(S) {
    const isLetter = c => /[a-z]/i.test(c);
    const toggle = c => /[a-z]/.test(c) ? c.toUpperCase() : c.toLowerCase();

    let perms = [], n = S.length;
    function dfs(perm, i) {
        if (i === n) {
            perms.push(perm.join(''));
            return;
        }
        dfs([...perm, S[i]], i + 1);
        if (isLetter(S[i])) {
            dfs([...perm, toggle(S[i])], i + 1);
        }
    }

    dfs([], 0);
    return perms;
};

 letterCasePermutation = function(S) {
     let n = S.length;
     const isLetter = c => /[a-z]/i.test(c);
     const toggle = c => /[a-z]/.test(c) ? c.toUpperCase() : c.toLowerCase();
     let que = [''];
     for (let i = 0; i < n; i++) {
         let c = S[i];
         let nextQue = [];
         for (let prefix of que) {
            nextQue.push(prefix + c);
            if (isLetter(c)) nextQue.push(prefix + toggle(c));
         }
         que = nextQue
     }
     return que;
 };
```

---
## [Mininum Distance between BST Nodes](https://leetcode.com/problems/minimum-distance-between-bst-nodes/description/)
`一遍过` `BST` `in order`

1. preorder + Write to Array
> Time: O(nlgn)
> Space: O(n)
> Write all the values to an array, then sort it. The minimum > distance must occur between two adjacent values in the > sorted list.

2. In order traversal
> Time: O(n)
> Space: O(h)
> BST => In order
> In a binary search tree, an in-order traversal outputs the values of the tree in order. By remembering the previous value in this order, we could iterate over each possible difference, keeping the smallest one.

```javascript
var minDiffInBST = function(root) {
    let prev = null, minDiff = Infinity;

    function inOrder(node) {
        if (!node) return;
        inOrder(node.left);
        if (prev && Math.abs(prev - node.val) < minDiff) {
            minDiff = Math.abs(prev - node.val);
        }
        prev = node.val;
        inOrder(node.right);
    }

    inOrder(root);
    return minDiff;
};
```
---
## [Toeplitz Matrix](https://leetcode.com/problems/toeplitz-matrix/description/)

`一遍过` `matrix`

1. Group by Category
> It turns out two coordinates are on the same diagonal if and only if `r1 - c1 == r2 - c2`
> This leads to the following idea: remember the value of that diagonal as groups[r-c]. If we see a mismatch, the matrix is not Toeplitz; otherwise it is.
> Time: O(m * n)
> Space: O(m + n)

2. Compare With Top-Left Neighbor
> The matrix is Toeplitz if and only if all of these conditions are true for all (top-left to bottom-right) diagonals
> Every element belongs to some diagonal, and it's previous element (if it exists) is it's top-left neighbor. Thus, for the square (r, c), we only need to check `r == 0 OR c == 0 OR matrix[r-1][c-1] == matrix[r][c].`

```javascript
var isToeplitzMatrix = function(matrix) {
    let m = matrix.length, n = m === 0 ? 0 : matrix[0].length;
    //let diags = new Map();
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            let num = matrix[i][j];
            let diag = i - j;
            //if (diags.has(diag) && diags.get(diag) !== num) return false;
            //diags.set(diag, num);
            if (matrix[i][j] !== matrix[i - 1][j - 1]) return false;
        }
    }
    return true;
};
```
---
## [Jewels & Stones](https://leetcode.com/problems/jewels-and-stones/description/)

`一遍过` `hashset`

1. Brute Force
> For each stone, check whether it matches any of the jewels. We can check with a linear scan.
> Time : O(nj * ns)
> Space: O(1)

2. Hashset
> For each stone, check whether it matches any of the jewels. We can check efficiently with a Hash Set.
> Time: O(ns + nj)
> Space: O(nj)

```javascript
var numJewelsInStones = function(J, S) {
    let jewels = new Set(J);
    return S.split('').filter(x => jewels.has(x)).length;
};
```
---
## [Prime Number of Set Bits in Binary Representation](https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/description/)

`一遍过` `prime number` `bit opr`

1. 按照题意
>对 `[L,R]`之间的每个数计算set bit， 如果这个cnt是prime那么结果加1.
>prime计算的时候可以优化到`sqrt(x)`
>set bit 计算的时候也可以优化
>Time: O(R-L)
>Space: O(1)

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

## [Min cost climbing stairs](https://leetcode.com/problems/min-cost-climbing-stairs/description/)

`一遍过` `回味` `dp`

1. recursion + mem
2. dp with space O(n) 爬到stair i, 还未离开（付钱）
3. dp with space O(n) 爬到stair i, 离开（付钱）之后
4. dp with space O(1) 爬到stair i, 还未离开（付钱）
5. dp with space O(1) 爬到stair i, 离开（付钱）之后

```javascript
var minCostClimbingStairs = function(cost) {
    let n = cost.length;
    let cache = new Array(n + 2).fill(-1);
    function climbCost(start) {//从stair i出发，付钱之后的cost
        if (start >= n) return 0;
        if (cache[start] !== -1) return cache[start];
        cache[start] = Math.min(climbCost(start + 1), climbCost(start + 2)) + cost[start];
        return cache[start];
    }
    return Math.min(climbCost(0),climbCost(1));
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, dp = new Array(n + 1).fill(0);
    for (let i = 2; i <= n; i++) {//爬到stair i, 还未离开（付钱）之前的cost
        dp[i] = Math.min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
    }
    return dp[n];
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, f1 = 0, f2 = 0;
    for (let i = 2; i <= n; i++) {//爬到stair i, 还未离开（付钱）之前的cost
        [f1, f2] = [Math.min(f1 + cost[i - 1], f2 + cost[i - 2]), f1];
    }
    return f1;
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, dp = new Array(n + 1).fill(0);
    dp[0] = cost[0];
    dp[1] = cost[1];
    for (let i = 2; i < n; i++) {//爬到stair i, 离开（付钱）之后的cost
        dp[i] = Math.min(dp[i - 1], dp[i - 2]) + cost[i];
    }
    return Math.min(dp[n - 1], dp[n - 2]);
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, f2 = cost[0], f1 = cost[1];
    for (let i = 2; i < n; i++) {//爬到stair i, 离开（付钱）之后的cost
        [f1, f2] = [Math.min(f1, f2) + cost[i], f1];
    }
    return Math.min(f1, f2);
};
```
