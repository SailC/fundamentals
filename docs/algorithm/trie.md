## [longest word dictionary](./hashtable.md#longest-word-dictionary)

## [implement trie](https://leetcode.com/problems/implement-trie-prefix-tree/description/)

application of trie:

1. autocomplete
2. spell checker
3. ip routing (longest prefix matching)

why trie ?

hash table has O(1) read complexity , but it's not efficient in :

1. finding all keys with a common prefix
2. enumerating a dataset of strings in lexical order (hashset doesn't have order)
3. hash collision when key # is big , from O(1) -> O(n)

read time complexity O(m) , m is the key length
write time complexity O(m) , In the worst case newly inserted key doesn't share a prefix with the the keys already inserted in the trie. We have to add mm new nodes, which takes us O(m) space.

searching a key in a BST (balanced) costs (mlogn) n is the size of the tree.

```javascript
class TrieNode {
    constructor() {
        this.links = new Array(26).fill(null);
        this.end = false;
    }
}

var Trie = function() {
    this.root = new TrieNode();
};

/**
 * Inserts a word into the trie.
 * @param {string} word
 * @return {void}
 */
Trie.prototype.insert = function(word) {
    let node = this.root;
    for (let c of word) {
        let idx = c.charCodeAt(0) - 'a'.charCodeAt(0);
        if (!node.links[idx]) node.links[idx] = new TrieNode();
        node = node.links[idx];
    }
    node.end = true;
};

/**
 * Returns if the word is in the trie.
 * @param {string} word
 * @return {boolean}
 */
Trie.prototype.search = function(word) {
    let node = this._searchNode(word);
    return (node !== null) && node.end;
};

/**
 * Returns if there is any word in the trie that starts with the given prefix.
 * @param {string} prefix
 * @return {boolean}
 */
Trie.prototype.startsWith = function(prefix) {
    let node = this._searchNode(prefix);
    return node !== null;
};

Trie.prototype._searchNode = function(word) {
    let node = this.root;
    for (let c of word) {
        let idx = c.charCodeAt(0) - 'a'.charCodeAt(0);
        if (!node.links[idx]) return null;
        node = node.links[idx];
    }
    return node;
}
```

---

## [add and search word](https://leetcode.com/problems/add-and-search-word-data-structure-design/description/)

> since a wild card char `.` can represent 26 letters, we use dfs to enumerate all the possible case, if any of the case matches, the search is successful.
> we try to match a letter in the word at each node in the recursion tree.
> `edge case`
> when node is null, return false
> when word has all been matched, return node.isEnd.
> dfs usually leave the null/invalid handling to the edge cases
> go & prune

```javascript
WordDictionary.prototype.addWord = function(word) {
    let node = this.root;
    for (let c of word) {
        let i = c.charCodeAt(0) - 'a'.charCodeAt(0);
        if (!node.links[i]) node.links[i] = new TrieNode();
        node = node.links[i];
    }
    node.isEnd = true;
};

WordDictionary.prototype.search = function(word) {
    function dfs(node, word, start) {
        if (!node) return false;
        if (start === word.length) {
            return node.isEnd;
        }
        // node !== null && start < word.length;
        let c = word[start];
        let i = c.charCodeAt(0) - 'a'.charCodeAt(0);
        if (c !== '.') return dfs(node.links[i], word, start + 1);
        for (i = 0; i < 26; i++) {
            if (dfs(node.links[i], word, start + 1)) return true;
        }
        return false;
    }
    return dfs(this.root, word, 0);
};
```
