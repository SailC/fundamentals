## [flood-fill](https://leetcode.com/problems/flood-fill/description/)
`一遍过` `回味` `dfs/bfs`

1. bfs
> 产生儿子的同时就要change color，不然siblings 会产生相同的儿子，造成duplicates
2. dfs
> 用color来做判重，原路径（或者其他已经被访问过的节点）的颜色都已经改变，可用来免费判重

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/733-ep116.png)

```javascript
var floodFill = function(image, sr, sc, newColor) {
    let m = image.length, n = m === 0 ? 0 : image[0].length;
    if (m === 0 || n === 0) return image;

    const inRange = (i, j) => i >= 0 && i < m && j >= 0 && j < n;
    let color = image[sr][sc];

    function bfs(sr, sc, newColor) {

        if (newColor === color) return;

        let que = [[sr, sc]];
        image[sr][sc] = newColor;
        while (que.length > 0) {
            let [i, j] = que.shift();
            for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
                if (inRange(x, y) && image[x][y] === color) {
                    image[x][y] = newColor;
                    que.push([x, y]);
                }
            }
        }
    }

    bfs(sr, sc, newColor);
    return image;
};

floodFill = function(image, sr, sc, newColor) {
    let m = image.length, n = m === 0 ? 0 : image[0].length;
    if (m === 0 || n === 0 || newColor === image[sr][sc]) return image;
    let color = image[sr][sc];
    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    (function dfs(i, j) {
        if (outOfBound(i, j) || image[i][j] !== color) return;
        image[i][j] = newColor;
        for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) dfs(x, y);
    })(sr, sc);
    return image;
};
```
---
## [number of islands](https://leetcode.com/problems/number-of-islands/description/)
`一遍过` `回味` `dfs/bfs`

1. `dfs`
for each remaining island, flood it with `bfs` or `dfs`. Each flood destroy a island. count how many island you can flood.

2. `careful about bfs`
The idea is that if you push all the pair into a queue before mark the grid, the same points might be pushed into queue by the siblings multiple times. `dfs` doesn't have this problem as the adj nodes are flooded immediately. A better way to solve this is to `mark & flood`, so that the runtime is still O(m * n)

```javascript
var numIslands = function(grid) {
    if (grid === null || grid.length === 0) return 0;
    let m = grid.length, n = grid[0].length;

    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    function dfs(i, j) {
        if (outOfBound(i, j) || grid[i][j] === '0') return;
        grid[i][j] = '0';
        for (let [x, y] of [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]) dfs(x, y);
    }

    function bfs(i, j) {
        let que = [[i, j]];
        grid[i][j] = '0';
        while (que.length > 0) {
            let [i, j] = que.pop();
            for (let [x, y] of [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]) {
                if (outOfBound(x, y) || grid[x][y] === '0') continue;
                grid[x][y] = '0';
                que.push([x, y]);
            }
        }
    }

    let cnt = 0;
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === '1') {
                cnt++;
                // dfs(i, j);
                bfs(i, j);
            }
        }
    }
    return cnt;
};
```
---
## [Max area of islands](https://leetcode.com/problems/max-area-of-island/description/)

`一遍过` `回味` `dfs/bfs`

```javascript
var maxAreaOfIsland = function(grid) {
    let m = grid.length, n = m === 0 ? 0 : grid[0].length;
    let maxArea = 0;

    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    function dfs(i, j) {
        if (outOfBound(i, j) || grid[i][j] === 0) return 0;
        grid[i][j] = 0;
        let cnt = 1;
        for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
            cnt += dfs(x, y);
        }
        return cnt;
    }

    function bfs(i, j) {
        let que = [[i, j]];
        grid[i][j] = 0;
        let cnt = 0;
        while (que.length > 0) {
            let [i, j] = que.shift();
            cnt++;
            for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
                if (outOfBound(x, y) || grid[x][y] === 0) continue;
                grid[x][y] = 0;
                que.push([x, y]);
            }
        }
        return cnt;
    }

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === 1) {
                //maxArea = Math.max(maxArea, dfs(i, j));
                maxArea = Math.max(maxArea, bfs(i, j));
            }
        }
    }
    return maxArea;
};
```

---
## [Friend Circles](https://leetcode.com/problems/friend-circles/description/)

`一遍过` `回味` `dfs/bfs` `UF`

1. dfs
> The given matrix can be viewed as the Adjacency Matrix of a graph. our problem reduces to the problem of finding the number of connected components in an undirected graph.
> from the graph, we can see that the components which are connected can be reached starting from any single node of the connected group. Thus, to find the number of connected components, we start from every node which isn't visited right now and apply DFS starting with it. We increment the countcount of connected components for every new starting node
> Time: `O(n^2)`
2. bfs
> Same idea. We increment the countcount of connected components whenever we need to start off with a new node as the root node for applying BFS which hasn't been already visited.
> Time: `O(n^2)` Each cell in adj matrix is visited once.
3. UF
> We traverse over all the nodes of the graph. For every node traversed, we traverse over all the nodes directly connected to it and assign them to a single group which is represented by their parentparent node
> At the end, we find the number of groups, or the number of parent nodes.
> Time: `O(n ^3)` We traverse over the complete matrix once. Union and find operations take O(n)O(n) time in the worst case.

```javascript
var findCircleNum = function(M) {
    let n = M.length;
    let cnt = 0;
    let visited = new Array(n).fill(false);

    function dfs(i) {
        if (visited[i]) return;
        visited[i] = true;
        for (let j = 0; j < n; j++) {
            if (j !== i && M[i][j]) dfs(j);
        }
    }

    function bfs(i) {
        let que = [i];
        visited[i] = true;
        while (que.length > 0) {
            let i = que.shift();
            for (let j = 0; j < n; j++) {
                if (j !== i && M[i][j] && !visited[j]) {
                    visited[j] = true;
                    que.push(j)
                }
            }
        }
    }

    for (let i = 0; i < n; i++) {
        if (!visited[i]) {
            //dfs(i);
            bfs(i);
            cnt++;
        }
    }
    return cnt;
};

var findCircleNum = function(M) {
    let uf = new UF(M.length);
    for (let i = 0; i < M.length; i++) {
        for (let j = 0; j < M[i].length; j++) {
            if (i < j && M[i][j] === 1) {
                uf.union(i, j);
            }
        }
    }
    return uf.size;
};
```

---

## [letter combination of a phone number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/)

```
`edge case`
1. `start === digits.length` running out of input string
2. current combination is not empty

`how to dfs`
manually create candidates dictionary. each letter can be used only once so need to increase the position on each level.
```

```javascript
var letterCombinations = function(digits) {
    let buttons = ['', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz'];
    let combs = [];
    function dfs(start, comb) {
        if (start === digits.length) {
            if (comb.length > 0) combs.push(comb);
            return;
        }
        for (let c of buttons[digits[start]]) {
            dfs(start + 1, comb + c);
        }
    }
    dfs(0, '');
    return combs;
};
```
---

## [subsets](https://leetcode.com/problems/subsets/description/)

```
input: `distinct integer` -> no dup in the same level
the solution set must not contain dup subsets -> can't go backward.
add partial solution to the results in each dfs node.
```

```javascript
var subsets = function(nums) {
    let results = [];
    function dfs(start, result) {
        results.push([...result]);
        for (let i = start; i < nums.length; i++) {
            result.push(nums[i]);
            dfs(i + 1, result);
            result.pop();
        }
    }
    dfs(0, []);
    return results;
};
```
---

## [subsets II](https://leetcode.com/problems/subsets-ii/description/)

```
`input contain duplicates` -> sort to dedup
```

```javascript
var subsetsWithDup = function(nums) {
    let results = [];
    nums.sort((a, b) => a - b);
    function dfs(start, result) {
        results.push([...result]);
        for (let i = start; i < nums.length; i++) {
            if (i > start && nums[i] === nums[i - 1]) continue;
            result.push(nums[i]);
            dfs(i + 1, result);
            result.pop();
        }
    }
    dfs(0, []);
    return results;
};
```
---

## [remove invalid paretheses](https://leetcode.com/problems/remove-invalid-parentheses/description/)

![](https://static.notion-static.com/d9a93428-ff70-4e7f-a22d-9b60affe77b3/Screen_Shot_2017-12-30_at_10.55.11_PM.png)

![](https://static.notion-static.com/35dcf76a-c94b-42c2-8ebe-ec8cab0a684f/Screen_Shot_2017-12-30_at_11.00.30_PM.png)

```javascript
var removeInvalidParentheses = function(s) {
    let result = [];
    let que = [s];
    let found = false;
    let visited = new Set([s]);
    while (que.length > 0 && !found) {
        let nextQue = [];
        for (let str of que) {
            if (isValid(str)) {
                found = true;
                result.push(str);
            } else {
                for (let i = 0; i < str.length; i++) {
                    if (i > 0 && str[i] === str[i - 1]) {
                        continue;
                    }
                    let tmp = `${str.slice(0, i)}${str.slice(i + 1)}`;
                    if (!visited.has(tmp)) {
                        nextQue.push(tmp);
                        visited.add(tmp);
                    }
                }
            }
        }
        que = nextQue;
    }
    return result;
};

var removeInvalidParentheses = function(s) {
    let [l, r] = getDeleteNum(s);
    let results = [];
    function dfs(s, start, l, r) {
        if (l === 0 && r === 0) {
            if (isValid(s)) results.push(s);
            return;
        }

        for (let i = start; i < s.length; i++) {
            if (i > start && s[i] === s[i - 1]) continue;
            if (s[i] !== '(' && s[i] !== ')') continue;
            if (r > 0 && s[i] === ')') {
                //bug1: erase i not 0
                dfs(s.slice(0, i) + s.slice(i + 1), i, l, r - 1);
            } else if (l > 0 && s[i] === '(') {
                dfs(s.slice(0, i) + s.slice(i + 1), i, l - 1, r);
            }
        }
    }
    dfs(s, 0, l, r);
    return results;
};

function isValid(s) {
    let cnt = 0;
    for (let c of s) {
        if (c === '(') {
            cnt++;
        } else if (c === ')') { //bug2: other char doens't count as )
            cnt--;
        }
        if (cnt < 0) return false;
    }
    return cnt === 0;
}

function getDeleteNum(s) {
    let l = 0, r = 0; //left paren to delete , right paren to delete
    for (let c of s) {
        if (c === '(') {
            l++;
        } else if (c === ')') { //bug3: other char doesn't count as )
            if (l === 0) {
                r++;
            } else {
                l--;
            }
        }
    }
    return [l, r];
}
```
---

## [expression add operators](https://leetcode.com/problems/expression-add-operators/description/)

> +, - 容易理解
> * 的时候要将之前的因子归零，然后加上之前的因子和cur的乘积，
> +, -都可以重置因子，* 则可以更新因子

```javascript
var addOperators = function(num, target) {
    let result = [];
    if (num === null || num.length === 0) return result;
    const dfs = (start, expr, eval, multed) => {
        if (start === num.length) {
            if (eval === target) {
                result.push(expr);
            }
            return;
        }
        for (let i = start; i < num.length; i++) {
            if (i !== start && num[start] === '0') break;
            let cur = Number(num.slice(start, i + 1));
            if (start === 0) {
                dfs(i + 1, `${expr}${cur}`, cur, cur);
            } else {
                dfs(i + 1, `${expr}+${cur}`, eval + cur, cur);    
                dfs(i + 1, `${expr}-${cur}`, eval - cur, -cur);
                dfs(i + 1, `${expr}*${cur}`, eval - multed + multed * cur, multed * cur);
            }
        }
    };
    dfs(0, "", 0, 0);
    return result;
};
```

---

## [binary tree paths](https://leetcode.com/problems/binary-tree-paths/description/)

```javascript
var binaryTreePaths = function(root) {
    let paths = [];
    function dfs(node, path) {
        if (!node) return;
        if (!node.left && !node.right) {
            paths.push([...path, node.val].join('->'));
            return;
        }
        dfs(node.left, [...path, node.val]);
        dfs(node.right, [...path, node.val]);
    }
    dfs(root, []);
    return paths;
};
```
---

## [word search](https://leetcode.com/problems/word-search/description/)

```
`find if the word exists` -> check if path exists -> dfs
pick any point in the matrix to start dfs

`edge case`
when all chars in the `word` have been matched, return true.
if out of range return false.
if doesn't match the starting char, return false;

`how to dfs`
if match the starting char, dfs to the neighbors, if any of the neighbor path is true, return true.

`dedup`
when match a char, set the grid[i][j] = '.' , when dfs return, reset it to its original value. this is used to prevent the cycle.
```

```javascript
var exist = function(board, word) {
    if (board === null || board.length === 0) return false;
    let m = board.length, n = board[0].length;
    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;
    function dfs(i, j, start) {
        if (start === word.length) return true;
        if (outOfBound(i, j) || board[i][j] !== word[start]) return false;
        let tmp = board[i][j];
        board[i][j] = '.';
        for (let [x, y] of [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]) {
            if (dfs(x, y, start + 1)) return true;
        }
        board[i][j] = tmp;
        return false;
    }
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (dfs(i, j, 0)) return true;
        }
    }
    return false;
};
```

---

## [combinations](https://leetcode.com/problems/combinations/description/)

`edge case`
no target sum limit, only cnt limit
`comb.length === k` .

`how to dfs`
each number can be used only once, no dup in the input.
need to keep track of the last added num position.

```javascript
var combine = function(n, k) {
    let combs = [];
    function dfs(comb, start) {
        if (comb.length === k) {
            combs.push([...comb]);
            return;
        }
        for (let i = start; i <= n; i++) {
            comb.push(i);
            dfs(comb, i + 1);
            comb.pop(i);
        }
    }
    dfs([], 1);
    return combs;
};
```

---

## [combination sum](https://leetcode.com/problems/combination-sum/description/)

`edge case`
All numbers (including target) will be positive integers.
so `target === 0` can be used as a edge case, as it would be meaningless to add positive numbers to futhur increase the current combination sum.

`how to dfs`
The solution set must not contain duplicate combinations. Since each element can be used unlimited number of times, `(1,2,1)` will duplicate `(1,1,2)` so it's important to sort the nums and make sure dfs doesn't go backward.
Another benefit of sorting is that it can be used to prune the case where adding a number already make current combination sum out of limit. In that case, we can ignore the following candidates since they're all bigger and only make things worse.

```javascript
var combinationSum = function(candidates, target) {
    let combs = [];
    candidates.sort((a, b) => a - b);
    function dfs(start, comb, target) {
        if (target === 0) {
            combs.push([...comb]);
            return;
        }
        for (let i = start; i < candidates.length && candidates[i] <= target; i++) {
            comb.push(candidates[i]);
            dfs(i, comb, target - candidates[i]);
            comb.pop();
        }
    }
    dfs(0, [], target);
    return combs;
};
```

---

## [combination sum II](https://leetcode.com/problems/combination-sum-ii/description/)

`edge case`
same as CombSumI, since all the numbers are positive, it's ok to stop when `target === 0`

`how to dfs`
`CombSumI` allows each element to be used unlimited number of times. This problem only allows one time, which force us to keep track of the position the last element added to the combination.
Also this problem contains duplicate numbers in the input.
So it's important to skip duplicate candidates if they're possible to generate the same combination.
sort the array and skip the consecutive candidates. so on the same level, only dfs on the first element and skip the following duplicates.

```javascript
var combinationSum2 = function(candidates, target) {
    candidates.sort((a, b) => a - b);
    let combs = [];
    function dfs(start, comb, target) {
        if (target === 0) {
            combs.push([...comb]);
            return;
        }
        for (let i = start; i < candidates.length && candidates[i] <= target; i++) {
            if (i > start && candidates[i] === candidates[i - 1]) continue;
            comb.push(candidates[i]);
            dfs(i + 1, comb, target - candidates[i]);
            comb.pop();
        }
    }
    dfs(0, [], target);
    return combs;
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

## [factor combination](https://leetcode.com/problems/factor-combinations/description/)

`diff to combSums`

1. need to manually generate candiates (factors)
2. get target via mutiplication instead of sum
3. every number can be used unlimited number of times but sequence order don't matter.

`edge case`
1. `target === 1` , be careful don't add empty comb set to the result

`how to dfs`
factors are sorted so no need to sort it.
skip the factors bigger than target.
sequence order don't matter , need to keep the pos of last added num, can't go backwrad.

```javascript
var getFactors = function(n) {
    let factors = getAllFactors(n);
    let combs = [];
    function dfs(start, comb, target) {
        if (target === 1) {
            if (comb.length > 0) combs.push([...comb]);
            return;
        }
        for (let i = start; i < factors.length && factors[i] <= target; i++) {
            comb.push(factors[i]);
            dfs(i, comb, target / factors[i]);
            comb.pop();
        }
    }
    dfs(0, [], n);
    return combs;
};

function getAllFactors(n) {
    let factors = [];
    for (let i = 2; i < n; i++) {
        if (n % i === 0) factors.push(i);
    }
    return factors;
}
```

---

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

---

## [palindrome partitioning](https://leetcode.com/problems/palindrome-partitioning/description/)

edge case:
when used up the input string. string won't be used up if invalid token is encountered
very similar to restore ip address when constructing tokens

```javascript
var partition = function(s) {
    let palins = [];
    function dfs(start, palin) {
        if (start === s.length) {
            palins.push([...palin]);
            return;
        }
        for (let i = 1; start + i <= s.length; i++) {
            let token = s.slice(start, start + i);
            if (isValid(token)) {
                dfs(start + i, [...palin, token]);
            }
        }
    }
    dfs(0, []);
    return palins;
};

function isValid(token) {
    let lo = 0, hi = token.length - 1;
    while (lo < hi) {
        if (token[lo] !== token[hi]) return false;
        lo++;
        hi--;
    }
    return true;
}
```

---

## [permutation](https://leetcode.com/problems/permutations/description/)

edge case === a perm of n elements has been crated

start pointer stays the same for each level
use visited map to avoid duplicates

```javascript
var permute = function(nums) {
    if (nums.length === 0) return [];
    let perms = [];
    function dfs(perm, visited) {
        if (perm.length === nums.length) {
            perms.push([...perm]);
            return;
        }
        for (let i = 0; i < nums.length; i++) {
            if (visited.has(i)) continue;
            perm.push(nums[i]);
            visited.add(i);
            dfs(perm, visited);
            visited.delete(i);
            perm.pop();
        }
    }
    dfs([], new Set());
    return perms;
};
```

---

## [permutation ii](https://leetcode.com/problems/permutations-ii/description/)

判重的条件
`if (visited.has(i) || (i > 0 && nums[i] === nums[i - 1] && !visited.has(i - 1))) continue;`
要看前一个相同的元素在不在上一层，如果不在，那么dup

```javascript
var permuteUnique = function(nums) {
    if (nums.length === 0) return [];
    let visited = new Set();
    let perms = [];
    nums.sort((a, b) => a - b);
    function dfs(perm) {
        if (perm.length === nums.length) {
            perms.push([...perm]);
            return;
        }
        for (let i = 0; i < nums.length; i++) {
            if (visited.has(i) || (i > 0 && nums[i] === nums[i - 1] && !visited.has(i - 1))) continue;
            visited.add(i);
            perm.push(nums[i]);
            dfs(perm);
            perm.pop();
            visited.delete(i);
        }
    }
    dfs([]);
    return perms;
};
```

---

## [palindrom permutation II](https://leetcode.com/problems/palindrome-permutation-ii/description/)

key take away :
1. only generate possible palindrom
2. build palindrome from the smaller half
3. palin = [...firsthalf, odd, ...revFirstHalf]

```javascript
var generatePalindromes = function(s) {
    let cntMap = countLetters(s);
    const canPalindrome = m => [...m.entries()].filter(([k, v]) => v % 2 !== 0).length <= 1;
    if (!canPalindrome(cntMap)) return [];
    let [letters, oddLetter] = splitStr(cntMap);

    letters.sort();
    let perms = [];
    let visited = letters.map(x => false);
    function dfs(perm) {
        if (perm.length === letters.length) {
            let rev = [...perm].reverse();
            let newPerm = [...perm, oddLetter, ...rev].join('');
            perms.push(newPerm);
            return;
        }
        for (let i = 0; i < letters.length; i++) {
            if (i > 0 && letters[i] === letters[i - 1] && !visited[i - 1]) continue;
            if (visited[i]) continue;
            visited[i] = true;
            dfs([...perm, letters[i]]);
            visited[i] = false;
        }
    }
    dfs([]);
    return perms;
};

function countLetters(s) {
    let map = new Map();
    for (let c of s) {
        map.set(c, (map.get(c) || 0) + 1);
    }
    return map;
}

function splitStr(map) {
    let halfStr = [], oddLetter = '';
    for (let [c, cnt] of map.entries()) {
        if (cnt % 2 === 1) oddLetter = c;
        for (let i = 0; i < ~~(cnt / 2); i++) {
            halfStr.push(c);
        }
    }
    return [halfStr, oddLetter];
}
```

---


## [permuation sequence](https://leetcode.com/problems/permutation-sequence/description/)

math (除法) + permutation
current k determines which index to pick
For permutations of n, the first (n-1)! permutations start with 1, next (n-1)! ones start with 2, ... and so on. And in each group of (n-1)! permutations, the first (n-2)! permutations start with the smallest remaining number, ...

everyround we pick a index to add and decrease n by 1

```javascript
var getPermutation = function(n, k) {
    let nums = [];
    for (let i = 1; i <= n; i++) nums.push(i);
    let perm = [];
    k--;
    while (n > 0) {
        n--;
        let i = ~~(k / fac(n));
        k = k % fac(n);
        perm.push(nums[i]);
        nums.splice(i, 1);
    }
    return perm.join('');
};

var getPermutation = function(n, k) {
    function dfs(nums, pos, seq, size) {
        if (seq.length === n) {
            return seq.join('');
        }
        let fact = fac(size - 1);
        let i = ~~(pos / fact);
        let j = pos % fact;
        let num = nums[i];
        nums.splice(i, 1);
        return dfs(nums, j, [...seq, num], size - 1);
    }
    let nums = [];
    for (let i = 1; i <= n; i++) nums.push(i);
    return dfs(nums, k - 1, [], n);
};

function fac(n) {
    if (n === 0) return 1;
    return fac(n - 1) * n;
}
```
---

## [beautiful arrangement](https://leetcode.com/problems/beautiful-arrangement/description/)

permutation的变种，对每个permutation加上一个sanity check，只记录满足beautiful条件的permutation

```javascript
var countArrangement = function(N) {
    function dfs(visited) {
        if (visited.size === N) return 1;
        let cnt = 0;
        for (let i = 1; i <= N; i++) {
            if (visited.has(i)) continue;
            const isBeautiful = i => {
                let index = visited.size + 1;
                return (i % index === 0) || (index % i === 0);
            };   
            if (isBeautiful(i)) {
                visited.add(i);
                cnt += dfs(visited);
                visited.delete(i);
            }
        }
        return cnt;
    }
    return dfs(new Set());
};
```

---

## [android unlock patterns](https://leetcode.com/problems/android-unlock-patterns/description/)

topdown 比较容易想到。
Rules for a valid pattern:
1. Each pattern must connect at least m keys and at most n keys.
说明超过n个key的解就要prune
key num 属于 [m, n] cnt++

2. All the keys must be distinct.
说明如果visited.has(key) 那么这个key不是valid

3. If the line connecting two consecutive keys in the pattern passes through any other keys, the other keys must have previously selected in the pattern. No jumps through non selected key is allowed.
如果lastkey和curKey中间有key的话，visited.has(key)才是valid

使用dfs进行top down recursion，每次都尝试九个key，看看这个move合不合法，如果合法则继续递归。

`T = O(9 ^ n)`

优化，利用matrix的对称性，1, 3, 7, 9 一样， 2, 4, 6, 8 一样, 5一个.

Time Complexity : `O(n!)` where n is the maximum pattern length.
The algorithm computes each pattern once and no element can appear in the pattern twice. The time complexity is proportional to the number of the computed patterns. One upper bound of the number of all possible combinations is:
`T = Perm(9, m) + Perm(9, m + 1) +... + Perm(9, n)`
`Perm(n, k) = n! / (n - k)!`
`Perm(n, k) = Comb(n, k) * Perm(k, k)`

```javascript
var numberOfPatternsI = function(m, n, visited) {
    let cnt = 0;
    let keys = [...new Array(9).keys()];

    function dfs(lastKey, size) {
        if (size > n) return;
        if (size >= m) cnt++;
        for (let key of keys) {
            if (isValidMove(lastKey, key)) {
                visited.add(key);
                dfs(key, size + 1);
                visited.delete(key);
            }
        }
    }

    function isValidMove(lastKey, key) {
        //all keys must be distinct
        if (visited.has(key)) return false;
        if (lastKey === -1) return true;
        let [x, y] = [~~(lastKey / 3), lastKey % 3];
        let [i, j] = [~~(key / 3), key % 3];
        // check the case where there is middle element
        let dx = Math.abs(x - i), dy = Math.abs(y - j);
        if ((dx === 0 && dy === 2) || (dx === 2 && dy === 0) || (dx === 2 && dy === 2)) {
            let mi = ~~((x + i) / 2), mj = ~~((y + j) / 2);
            let mid = 3 * mi + mj;
            return visited.has(mid);
        }
        return true;
    }
    let lastKey = visited.values().next().value;
    dfs(lastKey, 1);
    return cnt;
};

var numberOfPatterns = function(m, n) {
    return 4 * numberOfPatternsI(m, n, new Set([0])) + 4 * numberOfPatternsI(m, n, new Set([1])) + numberOfPatternsI(m, n, new Set([4]));
};
```

---

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
