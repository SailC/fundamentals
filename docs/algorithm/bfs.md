# BFS

## [word ladder](https://leetcode.com/problems/word-ladder/description/)

```
首先生儿子的时候，不能产生上一层的父节点或者本层的兄弟节点。用visited set来记录。
这里要注意判重的严苛程度：
1） 太松懈， 在循环本层的时候一个一个记录本层节点，这样有可能产生本层还没遍历到的兄弟节点。（不会产生父节点，因为上一层遍历的时候搞定了）
2） 太严格， 在生儿子之后立刻把儿子也放到visited set里面，这样不仅不能生成父节点和兄弟节点，连相同的儿子节点也无法生成（对II来说不可以这样，要求所有解）

正常的做法是
在遍历本层之前，先一次性把所有本层的元素加到visited里面，避免产生兄弟节点

transform 如果遍历所有wordList，然后一一和word比较看看diff是不是1，那么太耗时，O(wordListLen * wordLen) 。 O(26 * wordLen *O(1) ) 比较好，直接生成新的word然后去set找
```

```javascript
var ladderLength = function(beginWord, endWord, wordList) {
    let ladderLen = 1; //path only contains beginWord itself initially

    wordList = new Set(wordList);
    function transform(word) {
        let newWords = [];
        for (let i = 0; i < word.length; i++) {
            let letters = 'abcdefghijklmnopqrstuvwxyz'.split('');
            for (let c of letters) {
                if (c === word[i]) continue;
                let newWord = word.slice(0, i) + c + word.slice(i + 1);
                if (wordList.has(newWord)) newWords.push(newWord);
            }
        }
        return newWords;
    }
    // bfs transformation to construct word ladders
    let que = [beginWord];
    let visited = new Set();
    while (que.length > 0) {
        let nextQue = new Set();
        for (let word of que) visited.add(word);
        for (let word of que) {
            if (word === endWord) return ladderLen;
            for (let newWord of transform(word)) {
                if (visited.has(newWord)) continue;
                nextQue.add(newWord);
            }
        }
        que = [...nextQue];
        ladderLen++;
    }
    return 0;
};
```

---

## [word ladder II](https://leetcode.com/problems/word-ladder-ii/description/)

```
两题的区别是：
1) 判重的区别 2）II 除了bfs，还有dfs回溯

在遍历本层之前，先一次性把所有本层的元素加到visited里面，避免产生兄弟节点

然后nextQue使用set表示，保证不同家长可以产生相同儿子节点，但是下一层遍历只有一个儿子。
```

```javascript
var findLadders = function(beginWord, endWord, wordList) {
    wordList = new Set(wordList);
    let que = [beginWord];
    let visited = new Set([beginWord]);
    let parents = new Map();
    let found = false;
    while (que.length > 0 && !found) {
        let nextQue = new Set();
        visited = new Set([...visited, ...que]);
        for (let word of que) {
            if (word === endWord) {
                found = true;
                continue;
            }
            let words = getAdjWords(word, wordList, visited);
            for (let newWord of words) {
                nextQue.add(newWord);
                if (!parents.has(newWord)) {
                    parents.set(newWord, []);
                }
                parents.get(newWord).push(word)
            }
        }
        que = [...nextQue];
    }

    let results = [];
    dfs(beginWord, endWord, [endWord], results, parents);
    return results;
};

var dfs = (beginWord, word, path, results, parents) => {
    if (path.length > 0 && path[path.length - 1] === beginWord) {
        results.push(path.slice().reverse());
        return;
    }
    if (!parents.has(word)) {
        return;
    }
    for (let parent of parents.get(word)) {
        dfs(beginWord, parent, [...path, parent], results, parents);
    }
};

var getAdjWords = (word, wordList, visited) => {
    let letters = "abcdefghijklmnopqrstuvwxyz";
    let adjWords = [];
    for (let i = 0; i < word.length; i++) {
        let oldChar = word[i];
        for (let j = 0; j < 26; j++) {
            let adjWord = `${word.slice(0, i)}${letters[j]}${word.slice(i + 1)}`;
            if (adjWord !== word && wordList.has(adjWord) && !(visited.has(adjWord))) {
                adjWords.push(adjWord);
            }
        }
    }
    return adjWords;
};
```
---

## [binary tree level order traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/description/)

```
need level info to push to the result.
remember to map node to actual values before pushing to the result.
don't push null to the que.
```

```javascript
var levelOrder = function(root) {
    let results = [];
    if (!root) return [];
    let que = [root];
    while (que.length > 0) {
        let nextQue = [];
        results.push(que.map(node => node.val));
        for (let node of que) {
            if (node.left) nextQue.push(node.left);
            if (node.right) nextQue.push(node.right);
        }
        que = nextQue;
    }
    return results;
};
```
---

## [walls and gates](https://leetcode.com/problems/walls-and-gates/description/)

```
`flood and set`
starting for each gate , bfs to update the nearest distance to gate.

`how to bfs`
use hashset to store the nextQue to prevent duplicate children nodes.
childrens are only rooms (whose value is not 0 nor-1).
update the dist level by level.
for rooms in the current level, update it's value with the dist if necessary.

`prune`
if the dist so far is bigger than the current dist, then we can stop bfs from that node since the previous bfs would have already done it with a smaller dist.

这里判重有两处，一处是current que的两个node产生两个相同的儿子， 用hashset处理。另一处是nextLevel的node 产生parent level的节点，这一处因为dist一定变大，所以会被跳过。
```

```javascript
var wallsAndGates = function(rooms) {
    if (rooms === null || rooms.length === 0) return;
    let m = rooms.length, n = rooms[0].length;

    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    function bfs(i, j) {
        let que = [[i, j]], level = 0;
        while (que.length > 0) {
            let nextQue = [];
            for (let [i, j] of que) {
                for (let [x, y] of [[i + 1, j], [i - 1, j], [i, j - 1], [i, j + 1]]) {
                    if (outOfBound(x, y) || rooms[x][y] === -1 || level + 1 >= rooms[x][y]) continue;
                    rooms[x][y] = level + 1;
                    nextQue.push([x, y]);
                }
            }
            level++;
            que = nextQue;
        }
    }

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (rooms[i][j] === 0) bfs(i, j);
        }
    }
};
```

---

## [binary tree zigzag level order traversal](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/)

```javascript
var zigzagLevelOrder = function(root) {
    if (!root) return [];
    let results = [], que = [root], forward = true;
    while (que.length > 0) { //bfs
        let result = que.map(node => node.val);
        results.push(forward ? result : result.reverse());
        forward = !forward;
        let nextQue = [];
        for (let node of que) {
            if (node.left) nextQue.push(node.left);
            if (node.right) nextQue.push(node.right);
        }
        que = nextQue;
    }
    return results;
};
```
