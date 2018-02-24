## [two sum](https://leetcode.com/problems/two-sum/description/)
`一遍过` `回味`

1. bruteforce
> for each nums[i], check if there's a num[j] (j > i) that nums[i] + nums[j] === target.
> if so, return [i, j]
> Time: O(n^2)
> space: O(1)

2. hashtable
> Use hashtable to save the `number to index` mapping
> Time: O(n)
> Space: O(n)

```javascript
var twoSum = function(nums, target) {
    let map = new Map();
    for (let i = 0; i < nums.length; i++) {
        let num = nums[i];
        if (map.has(target - num)) return [map.get(target - num), i];
        map.set(num, i);
    }
    return -1;
};
```
---
## [longest word dictionary](https://leetcode.com/problems/longest-word-in-dictionary/description/)

0. brute force
> For each word, check if all prefixes word[:k] are present. We can use a Set structure to check this quickly.
> time : O(n * w * w) , for each word, for each prefix , create that prefix

1. sort + check O(nlgn) n is the # of words in the dictionary
> 先将words按长短（等长看alphabetical order）排序
> 然后对于每一个新的word，看看他的前缀 `word[0: len -1)` 是不是已经被visited过 （被visited 过的word的所有前缀都保证被visited 过，是一步一步堆积出来的）

2.
> Put every word in a trie, then depth-first-search from the start of the trie, only searching nodes that ended a word. Every node found (except the root, which is a special case) then represents a word with all it's prefixes present. （自动满足堆积条件)
> Time: O(w1 + w2 + w3 + ...) w1 means the length of word1
> space: O(n * w * 26) = # of trie nodes * 26 = # of distinct chars * 26

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/720-ep109.png)

```javascript
var longestWord = function(words) {
     words = new Set(words);
        words.add('');
        let longest = '';
        for (let word of words) {
            let n = word.length;
            if (n < longest.length || (n === longest.length && word > longest)) continue;//pruning
            let valid = true;
            for (let i = 0; i < n && valid; i++) {
                let prefix = word.slice(0, i);
                if (!words.has(prefix)) valid = false;
            }
            if (valid) longest = word;
        }
        return longest;
};

longestWord = function(words) {
    words.sort((word1, word2) => {
        if (word1.length < word2.length) return -1;
        if (word1.length > word2.length) return 1;
        return word1 < word2 ? -1 : (word1 > word2 ? 1 : 0);
    });
    let longest = '';
    let visited = new Set(['']);
    for (let word of words) {
        let prev = word.slice(0, word.length - 1);//if s[0:k - 1] is visited, all the previous substring must be visited as well
        if (visited.has(prev)) {
            visited.add(word);
            if (word.length > longest.length) {
                longest = word;
            }
        }
    }
    return longest;
};

class TrieNode {
    constructor() {
        this.links = new Array(26).fill(null);
        this.isWord = false;
    }
}

function add(root, word) {
    let cur = root;
    for (let c of word) {
        let i = c.charCodeAt(0) - 'a'.charCodeAt(0);
        if (!cur.links[i]) cur.links[i] = new TrieNode();
        cur = cur.links[i];
    }
    cur.isWord = true;
}

var longestWord = function(words) {
    let root = new TrieNode();
    root.isWord = true;
    for (let word of words) add(root, word);
    let result = null;
    (function dfs(node, word) {
        if (!node || !node.isWord) return;
        if (result === null || word.length > result.length) result = word;
        for (let i = 0; i < 26; i++) {
            let c = String.fromCharCode('a'.charCodeAt(0) + i);
            dfs(node.links[i], word + c);
        }
    })(root, '');
    return result;
};
```
