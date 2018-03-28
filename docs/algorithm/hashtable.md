
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
---
## [Sentence Similarity](https://leetcode.com/problems/sentence-similarity/description/)
`一遍过` `hashset`

1.hashset
> To check whether words1[i] and words2[i] are similar, either they are the same word, or (words1[i], words2[i]) or (words2[i], words1[i]) appear in pairs.
> To check whether (words1[i], words2[i]) appears in pairs quickly, we could put all such pairs into a Set structure.
> Time Complexity:  O(|pairs| + |words1|)

```javascript
var areSentencesSimilar = function(words1, words2, pairs) {
    let m = words1.length, n = words2.length;
    if (m !== n) return false;
    let set = new Set();
    const getKey = (w1, w2) => `${w1}:${w2}`;

    for (let [w1, w2] of pairs) {
        set.add(getKey(w1, w2));
        set.add(getKey(w2, w1));
    }
    for (let i = 0; i < n; i++) {
        let w1 = words1[i], w2 = words2[i];
        let key = getKey(w1, w2);
        if (w1 !== w2 && !set.has(key)) return false;
    }
    return true;
};
```
---

## [group anagram](https://leetcode.com/problems/group-anagrams/description/)

1. Normalize by sorting + HashTable
> two anagrams share the same characters, sort them will result in the same word (we call it normalized key).
> Use the normalized key as the key of the hashtable, and the value of the hashtable is the list of the orginal words sharing the same normalized key.
return the list of values of the hashmap, which can be done by `[...map.values()]`
> - Time: O(n * m lgm) n is the # of words, m is the length of each word
> - Space: O(n)

2. Normalize by couting + HashTable
> change the normalization function from sorting to counting. Make a array of size 26 to save the cnt of each characters in the word, and join the array with a separater to avoid confusion (e.g. a:1 b:2 v.s. a:12 b:0)
> - Time: O(n * m)
> - Space: O(n)

```javascript
var groupAnagrams = function(strs) {
    const normalize = word => word.split('').sort().join('');
    let map = new Map(); // map normalized word => a list of original words
    for (let word of strs) {
        let key = normalize(word);
        if (!map.has(key)) map.set(key, []);
        map.get(key).push(word);
    }
    return [...map.values()];
};

var groupAnagrams = function(strs) {
    // const normalize = word => word.split('').sort().join('');
    const normalize = word => {
        let keyArr = new Array(26).fill(0);
        for (let c of word) keyArr[c.charCodeAt(0) - 'a'.charCodeAt(0)]++;
        return keyArr.join('#');
    };
    let map = new Map(); // map normalized word => a list of original words
    for (let word of strs) {
        let key = normalize(word);
        if (!map.has(key)) map.set(key, []);
        map.get(key).push(word);
    }
    return [...map.values()];
};
```
---
## [longest consecutive sequence](https://leetcode.com/problems/longest-consecutive-sequence/description/)

1. HashSet + Bruteforce
> We use a hashset to save all the appeared number, this can help delete the duplicates, which only complicates the problem.
> Then we iterate through all the number one by one, for each number we try to extend it to both left & right as much as possible by checking if the boundaries are in the hashset.
> Time : O(n ^ 2)
> Space: O(n)
> Optimization: instead of extend it both left & right direction, we only consider on direction. Let's say, we only consider to extend the number to the right as much as possible. e.g. [1,2,3,4] when we pick 3 as the starting point, we don't look backward, as the same sequence can be constructed by starting with 1 or 2.

2. HashSet + Skipping meaningless element
> As we can see from the optimization above, when we pick 3, we don't look backward, because the same seqence can be constructed by 2. And we don't have to look forward either for 3, because the same sequence can also start with 2.
> So we can totally skip the element whose previous element appeared in the Hashset, which means every increasing seq started by that element can be constructed by starting with the previous element.
> Time: O(n) we visited each element exactly once. 2 cases here, `num` is either visited as the start of the increasing seq, or visited during the extension of that increasing seq. If it's in the middle of the ICS, it won't be visited twice since it will be skipped.
> Space: O(n)

```javascript
var longestConsecutive = function(nums) {
    let visited = new Set(nums);
    let maxCnt = 0;
    for (let num of nums) {
        let cnt = 0;
        if (visited.has(num - 1)) continue;
        while (visited.has(num)) {
            cnt++;
            num++;
        }
        maxCnt = Math.max(maxCnt, cnt);
    }
    return maxCnt;
};
```
---
## [brick wall](https://leetcode.com/problems/brick-wall/description/)

1. hashtable
> cross the least bricks ==> hits the most boundaries
use a hashtable to map the boundaries to the number of bricks with that boundary.

```javascript
var leastBricks = function(wall) {
    let cols = new Map();
    let maxCnt = 0;
    for (let row of wall) {
        let col = 0;
        for (let i = 0; i < row.length - 1; i++) {
            col += row[i];
            cols.set(col, (cols.get(col) || 0) + 1);
            maxCnt = Math.max(maxCnt, cols.get(col));
        }
    }
    return wall.length - maxCnt;
};
```
---
## [palindrom pairs](https://leetcode.com/problems/palindrome-pairs/description/)

> The basic idea is to check each word for prefixes (and suffixes) that are themselves palindromes. If you find a prefix that is a valid palindrome, then the suffix reversed can be paired with the word in order to make a palindrome. It’s better explained with an example.

> words = ["bot", "t", "to"]
> Starting with the string “bot”. We start checking all prefixes. If "", "b", "bo", "bot" are themselves palindromes. The empty string and “b” are palindromes. We work with the corresponding suffixes (“bot”, “ot”) and check to see if their reverses (“tob”, “to”) are present in our initial word list. If so (like the word to"to"), we have found a valid pairing where the reversed suffix can be prepended to the current word in order to form “to” + “bot” = “tobot”.

 > Note that when considering suffixes, we explicitly leave out the empty string to avoid counting duplicates. That is, if a palindrome can be created by appending an entire other word to the current word, then we will already consider such a palindrome when considering the empty string as prefix for the other word.

 ```javascript
 var palindromePairs = function(words) {
    let map = new Map();
    for (let i = 0; i < words.length; i++) map.set(words[i], i);
    let pairs = [];

    for (let [word, idx] of map) {
        let n = word.length;
        for (let i = 0; i <= n; i++) {
            let prefix = word.slice(0, i);
            let suffix = word.slice(i);
            if (isPalin(prefix)) {
                suffix = suffix.split('').reverse().join('');
                if (suffix !== word && map.has(suffix)) {
                    pairs.push([map.get(suffix), idx]);
                }
            }
            // avoid prefix = '' , suffix = word
            // prefix = word , suffix = ''
            if (i < n && isPalin(suffix)) {
                prefix = prefix.split('').reverse().join('');
                if (prefix !== word && map.has(prefix)) {
                    pairs.push([idx, map.get(prefix)]);
                }
            }
        }
    }

    return pairs;
};

function isPalin(s) {
    return s.split('').reverse().join('') === s;
}
```
---
## [Array nesting](https://leetcode.com/problems/array-nesting/description/)

> 按照nesting的规则，N个index可以被划分为several 连通分量，我们只需要计算每个连通分量的cnt就可以了
> 用visited数组记录已经被访问过index，只更新连通分量当中首次被访问到的那个index的cnt

```javascript
var arrayNesting = function(nums) {
    let cntMap = new Map();
    function S(i) {
        if (cntMap.has(i)) return cntMap.get(i);
        let cnt = 0, visited = new Set();
        for (; !visited.has(i); i = nums[i]) {
            cnt++;
            visited.add(i);
        }
        for (let j of visited) cntMap.set(j, cnt);
        return cnt;
    }

    let longest = 0;
    for (let i = 0; i < nums.length; i++) longest = Math.max(longest, S(i));
    return longest;
};

arrayNesting = function(nums) {
    let visited = new Set();
    let longest = 0;
    for (let i = 0; i < nums.length; i++) {
        if (visited.has(i)) continue;
        let cnt = 0;
        while (!visited.has(i)) {
            cnt++;
            visited.add(i);
            i = nums[i];
        }
        longest = Math.max(longest, cnt);
    }
    return longest;
};
```

---

## [isomorphic strings](https://leetcode.com/problems/isomorphic-strings/description/)

use two hash map to represent the mapping from s to t, and t to s.
if we found a char s[i] map to two different chars in t, or t[i] map to 2 diff chars in s, return false

another way is to use two arrays to store the last seen index of the char s[i] && t[i]. Initially everything is init to 0, (we haven't seen any of the chars yet). If any of the char appears for the first time, we set the seen index as the current index as there's nothing to tell at this point.

if any char appears for the second time or more, we want to make sure the same char doesn't map to two different chars in another string, so just check their indexing arr and see if
1. the char has been seen in the other array
2. the previous store position should be the same
If previously stored positions are different then we know that the fact they're occuring in the current i-th position simultaneously is a mistake.

```javascript
var isIsomorphic = function(s, t) {
    let mapS = new Map(), mapT = new Map();
    for (let i = 0; i < s.length; i++) {
        if (!mapS.has(s[i])) {
            mapS.set(s[i], t[i]);
        } else {
            if (mapS.get(s[i]) !== t[i]) return false;
        }
        if (!mapT.has(t[i])) {
            mapT.set(t[i], s[i]);
        } else {
            if (mapT.get(t[i]) !== s[i]) return false;
        }
    }
    return true;
};

var isIsomorphic = function(s, t) {
    let indexS = new Array(256).fill(-1),
        indexT = new Array(256).fill(-1);
    for (let i = 0; i < s.length; i++) {
        let charCodeS = s.charCodeAt(i);
        let charCodeT = t.charCodeAt(i);
        if (indexS[charCodeS] !== indexT[charCodeT]) return false;
        indexS[charCodeS] = i;
        indexT[charCodeT] = i;
    }
    return true;
};
```

---

## [palindrome permutation](https://leetcode.com/problems/palindrome-permutation-ii/description/)

```javascript
var canPermutePalindrome = function(s) {
    let set = new Set(); //char
    for (let c of s) {
        if (set.has(c)) {
            set.delete(c);
        } else {
            set.add(c);
        }
    }
    return set.size <= 1;
};
```

---
