# Linkedin


## onsite

```javascript
/**
Input: a number (n)
Output: Return all the factors of it

12 => 2*6, 3*4, 2*2*3

*/



// [2 * 6, 3 * 4, 2 * 2 * 3]
// [[2, 6], [3, 4], [2, 2, 3]]

// 2, 3, 4, 5, 6....11

// 32 = 2 * 2 * 2 * 2 * 2 = 2 ^ 5  O(lgn)

// e.g. 2 * 2 * 3
//      3 * 2 * 2
        3 * 3


        start = 1                  [2] [3]  [4]  [6]
                                 [2,2]
                               [2, 2, 2] [2, 2, 3]

12 [2, 3, 4, 6] k total k = 4;

 k
 k ^ 2
 k ^ 3
 .....
 k ^ lgn
 total = (1 + 2 + 3 + ... + lgn) * k = k (lgn)(lgn)


function allFactors(num) {

     let results = [];

     function dfs(factors, product, start) {
         if (product === num) {
             results.push([...factors]);
             return;
         }
         for(let i = start; i < num; i++) {
             if (proudct * i > num) continue;
             if (num % i !== 0) continue;
             factors.push(i);
             dfs(factors, product * i, i);
             factors.pop();
         }
     }

     dfs([], 1, 2);

     return results;
}
```

---

## LC 52

| Problem        | tags           | pass  |
| ------------- |:-------------:| -----:|
| [max stack](./stack.md#max-stack) | design | :) |
| [insert delete get random ](./design.md#insert-delete-getrandom-o1) | design |  |
| [two sum](./array.md#two-sum) | hashtable | :) |
| [two sum II](./array.md#two-sum-ii) | hashtable | :) |
| [two sum III](./design.md#two-sum-iii) | hashtable |  |
| [isomorphic string](./hashtable.md#isomorphic-strings) | hashtable | :) |
| [valid number](./string.md#valid-number) | string |  |
| [text justification](./string.md##text-justification) | string |  |
| [evaluate reverse polish notation](./stack.md#evaluate-reverse-polish-notation) | stack | :) |
| [binary search tree iterator](./stack.md#binary-search-tree-iterator) | stack | :) |
| [sparse matrix multiplication](./array.md##sparse-matrix-multiplication) | array | :) |
| [shortest word distance](./array.md#shortest-word-distance) | array |  |
| [shortest word distance II](./array.md#shortest-word-distance-ii) | array |  |
| [shortest word distance III](./array.md#shortest-word-distance-iii) | array |  |
| [permutation](./dfs.md#permutation) | dfs |  |
| [permutation II](./dfs.md#permutation-ii) | dfs |  |
| [factor combination](./dfs.md#factor-combination) | dfs |  |
| [nested list weight sum](./dfs.md#nested-list-weight-sum) | dfs |  |
| [nested list weight sum ii](./dfs.md#nested-list-weight-sum-ii) | dfs |  |
| [max depth of binary tree](./tree.md#max-depth-of-binary-tree) | bottom up tree | :) |
| [find leaves of binary tree](./tree.md##find-leaves-of-binary-tree) | bottom up tree | :) |
| [binary tree upside down](./tree.md#binary-tree-upside-down) | bottom up tree |  |
| [lowest common ancestor binary tree](./tree.md#lowest-common-ancestor-of-a-binary-tree) | bottom up tree |  |
| [lowest common ancestor bst](./tree.md#lowest-common-ancestor-of-a-bst) | top down tree |  |
| [symmetric tree](./tree.md#symmetric-tree) | top down tree | :) |
| [word ladder](./bfs.md#word-ladder) | bfs |  |
| [word ladder ii](./bfs.md#word-ladder-ii) | bfs |  |
| [find largest value in each tree row](./tree.md#find-largest-value-in-each-tree-row) | bfs | :) |
| [binary tree level order traversal](./tree.md#binary-tree-level-order-traversal) | bfs | :) |
| [binary tree zigzag level order traversal](./bfs.md##binary-tree-zigzag-level-order-traversal) | bfs | :) |
| [serialize and deserialize binary tree](./tree.md#serialize-and-deserialize-binary-tree) | tree |  |
| [max point on a line](./geometry.md##max-points-on-a-line) | geometry | :( |
| [sum of square number](./math.md#sum-of-square-numbers) | math | :) |
| [insert interval](./sorting.md#insert-interval) | sort |  |
| [merge interval](./sorting.md##merge-intervals) | sort |  |
| [merge k sorted list](./linked-list.md#merge-k-sorted-lists) | merge |  |
| [merge two sorted list](./linked-list.md#merge-two-sorted-list) | merge | :) |
| [repeated dns sequence](./sliding-window.md##repeated-dna-sequence) | sliding window | :) |
| [minimum window substring](./sliding-window.md#minimum-window-substring) | sliding window |  |
| [can place flowers](./greedy.md#can-place-flowers) | greedy |  |
| [find the celebrity](./greedy.md#find-celebrities) | greedy |  |
| [maximum subarray](./dp.md#maximum-subarray) | dp |  |
| [can I win](./dp.md#can-i-win) | dp | :( |
| [palindromic substring](./dp#palindrom-substring) | dp |  |
| [second min node in a binary tree](./tree.md#second-minimum-node-in-a-binary-tree) | dp | :) |
| [partition to k equal sum subsets](./dp.md#partition-to-k-equal-sum-subset) | dp |  |
| [maximum product subarray](./dp.md#maximum-product-subarray) | dp | :) |
| [paint house](./dp.md#paint-house) | dp |  |
| [house robber](./dp.md#house-robber) | dp |  |
| [product of array except self](./array.md#product-of-array-except-self) | dp |  |
| [count different palindromic subsequences](./dp.md#count-different-palindrom-subsequences) | dp |  |
| [find smallest letter greater than target](./binary-search.md#find-smallest-letter-greater-than-target) | binary serach | :) |
| [pow(x, n)](./math.md#powxn) | binary search | :) |
| [valid perfect square](./binary-search.md#valid-perfect-square) | binary search | :) |
| [search in rotated sorted array](./binary-search.md#search-in-rotated-sorted-array) | binary search | :) |
| [search for a range](./binary-search.md#search-for-a-range) | binary search | :) |
