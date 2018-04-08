# huahua jiang


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
