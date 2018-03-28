## [serialize and deserialize binary tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/description/)

`有思路` `盲区` `dfs/bfs` `recursion`

1. `dfs serialization`
> since it's a binary tree (not a BST) , we need to keep track of the null pionters so we know what the tree look like.
> `edge case`
> node is null, push `#`.
> `how to dfs`
> push the node vallue, and recursive to left and right.
> `how to decode`
> also with dfs, pick the first value as the root to return and recursively construct the left and right nodes.
> 注意，如果用中序遍历输出的话会导致同一个字符串可以有不同的解释（对应不同的二叉树) `#0#0#` 你不知道左子树到底是 `#0#` or `#` , 但是如果是preorder你一定知道下一个节点是 `#` .

2. bfs
> 稍微麻烦一点，先用首字符建一个root，push到que里面
> 然后每次从que shift出来一个node，将其左右child nodes建立起来，如果不为空则入队列
> 每次建立新node都要读取data
> 也是preorder ，只不过是bfs

```javascript
var serialize = function(root) {
    let result = [];
    function dfs(node) {
        if (!node) {
            result.push('#');
            return;
        }
        result.push(node.val);
        dfs(node.left);
        dfs(node.right);
    }
    dfs(root);
    return result.join(',');
};

var deserialize = function(data) {
    let values = data.split(',');
    function dfs() {
        if (values.length === 0) return null;
        let val = values.shift();
        if (val === '#') return null;
        let node = new TreeNode(Number(val));
        node.left = dfs();
        node.right = dfs();
        return node;
    }
    return dfs();
}

var serialize = function(root) {
    let encoded = [];
    let que = [root];
    while (que.length > 0) {
        let node = que.shift();
        if (!node) {
            encoded.push('#');
        } else {
            encoded.push(node.val);
            que.push(node.left);
            que.push(node.right);
        }
    }
    return encoded.join(',');
};

var deserialize = function(data) {
    let decoded = data.split(',');
    let val = decoded.shift();
    let root = val === '#' ? null : new TreeNode(Number(val));
    if (root === null) return null;
    let que = [root];
    while (que.length > 0) {
        let node = que.shift();
        let leftVal = decoded.shift(), rightVal = decoded.shift();
        node.left = leftVal === '#' ? null : new TreeNode(Number(leftVal));
        node.right = rightVal === '#' ? null : new TreeNode(Number(rightVal));
        if (node.left) que.push(node.left);
        if (node.right) que.push(node.right);
    }
    return root;
}
```
---
## [Find Duplicate Subtrees](https://leetcode.com/problems/find-duplicate-subtrees/description/)
`无思路` `serialization` `回味`

1. dfs + serialization
>  dfs the tree, for each node, call serialization to encode the subtree and check the map
> Time: O(N ^ 2)
2. dfs alone
> combine dfs with serialization
> Perform a depth-first search, where the recursive function returns the serialization of the tree. At each node, record the result in a map, and analyze the map after to determine duplicate subtrees.
> Time: O(N)
3. add another map to map encoded string to uniq id to save some space

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/652-ep146-1.png)

```javascript
var findDuplicateSubtrees = function(root) {
    let result = [];
    let cntMap = new Map();
    function dfs(node) {
        if (!node) return;
        let encode = serialize(node);
        let cnt = cntMap.get(encode) || 0;
        if (cnt === 1) result.push(node);
        cntMap.set(encode, cnt + 1);
        dfs(node.left);
        dfs(node.right);
    }
    dfs(root);
    return result;
};

function serialize(root) {
    if (!root) return '#';
    let left = serialize(root.left), right = serialize(root.right);
    return `${root.val},${left},${right}`;
}

findDuplicateSubtrees = function(root) {
    let result = [];
    let cntMap = new Map();
    function dfs(node) {
        if (!node) return '#';
        let left = dfs(node.left),
            right = dfs(node.right);
        let encode = `${node.val},${left},${right}`;
        cntMap.set(encode, (cntMap.get(encode) || 0) + 1);
        if (cntMap.get(encode) === 2) result.push(node);
        return encode;
    }
    dfs(root);
    return result;
};

findDuplicateSubtrees = function(root) {
    let result = [];
    let cntMap = new Map();
    let gid = 1;
    let idxMap = new Map();
    function dfs(node) {
        if (!node) return 0;
        let left = dfs(node.left),
            right = dfs(node.right);
        let encode = `${node.val},${left},${right}`;
        if (!idxMap.has(encode)) idxMap.set(encode, gid++);
        let id = idxMap.get(encode);
        cntMap.set(id, (cntMap.get(id) || 0) + 1);
        if (cntMap.get(id) === 2) result.push(node);
        return id;
    }
    dfs(root);
    return result;
};
```
---
## [populating next right pointers in each node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node/description/)
```
Given the following perfect binary tree,
         1
       /  \
      2    3
     / \  / \
    4  5  6  7
After calling your function, the tree should look like:
         1 -> NULL
       /  \
      2 -> 3 -> NULL
     / \  / \
    4->5->6->7 -> NULL

```

```javascript
var connect = function(root) {
    if (!root) return;
    if (root.left) root.left.next = root.right;
    if (root.right && root.next) root.right.next = root.next.left;
    connect(root.left);
    connect(root.right);
};
```
---

## [populating next right pointers in each node II](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/description/)

```
先画图，然后遍历本层的linked list的同时构建下一层的linked list。
构建完毕之后，遍历下一层的linked list，一直到没有下一层为止。

初始条件本层的linkedlist就是一个root节点
```

```javascript
var connect = function(root) {
    while (root) {
        let head = new TreeLinkNode();
        let cur = head;
        for (let node = root; node; node = node.next) {
            if (node.left) {
                cur.next = node.left;
                cur = cur.next;
            }
            if (node.right) {
                cur.next = node.right;
                cur = cur.next;
            }
        }
        root = head.next;
    }
};
```
---

## [sum of left leaves](https://leetcode.com/problems/sum-of-left-leaves/description/)

```
need to know whether a node is a left leaf.
use prev to point to the last traversed node.
const isLeftLeaf = isLeaf && prev.left = node
```

```javascript
var sumOfLeftLeaves = function(root) {
    if (!root) return 0;
    let prev = null, sum = 0;
    const isLeaf = node => !node.left && !node.right;
    function preorder(node) {
        if (!node) return;
        if (isLeaf(node) && prev && prev.left === node) sum += node.val;
        prev = node;
        preorder(node.left);
        preorder(node.right);
    }
    preorder(root);
    return sum;
};

var sumOfLeftLeaves = function(root) {
    if (!root) return 0;
    let stack = [root];
    let prev = null;
    let sum = 0;
    const isLeaf = node => !node.left && !node.right;
    while (stack.length > 0) {
        let node = stack.pop();
        if (isLeaf(node) && prev && prev.left === node) sum += node.val;
        if (node.right) stack.push(node.right);
        if (node.left) stack.push(node.left);
        prev = node;
    }
    return sum;
};
```

----

## [average levels in binary tree](https://leetcode.com/problems/average-of-levels-in-binary-tree/description/)

```
Input:
    3
   / \
  9  20
    /  \
   15   7
Output: [3, 14.5, 11]
Explanation:
The average value of nodes on level 0 is 3,  on level 1 is 14.5, and on level 2 is 11. Hence return [3, 14.5, 11]
```

```javascript
var averageOfLevels = function(root) {
    let result = [];
    if (!root) return [];
    let que = [root];
    while (que.length > 0) {
        let sum = que.reduce((acc, node) => (acc + node.val), 0);
        result.push(sum / que.length);
        let nextQue = [];
        for (let node of que) {
            if (node.left) nextQue.push(node.left);
            if (node.right) nextQue.push(node.right);
        }
        que = nextQue;
    }
    return result;
};
```

---

## [binary tree vertical order traversal](https://leetcode.com/problems/binary-tree-vertical-order-traversal/description/)

```
`bfs traversal + col info for each nodes`
use map to map the col index to the list of nodes.

can't use dfs here as there is level oder requirement in each col array
```

```javascript
var verticalOrder = function(root) {
    let map = new Map(); //key: idx val: [val]
    if (root === null) return [];
    let que = [[root, 0]];
    while (que.length > 0) {
        let nextQue = [];
        for (let cur of que) {
            let [node, col] = cur;
            if (!map.has(col)) map.set(col, []);
            map.get(col).push(node.val);
            if (node.left) nextQue.push([node.left, col - 1]);
            if (node.right) nextQue.push([node.right, col + 1]);
        }
        que = nextQue;
    }

    let keys = [...map.keys()].sort((a, b) => a - b);
    return keys.map(key => map.get(key));
};
```
---

## [lowest common ancestor of a bst](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/description/)

```javascript
var lowestCommonAncestor = function(root, p, q) {
    if (!root) return null;
    if (root.val > Math.max(p.val, q.val)) return lowestCommonAncestor(root.left, p, q);
    if (root.val < Math.min(p.val, q.val)) return lowestCommonAncestor(root.right, p, q);
    return root;
};
```

---

## [lowest common ancestor of a binary tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/)

```
use a helper function to return the node if any of the node is in the subtree.

if both the left & right subtree contains a node, it means p and q are on the two sides of the root node, root is the LCS.
if p & q are in the same side, recurse to that side.
```

```javascript
var lowestCommonAncestor = function(root, p, q) {
    if (!root) return null;
    if (root === p) return p;
    if (root === q) return q;
    let left = lowestCommonAncestor(root.left, p, q);
    let right = lowestCommonAncestor(root.right, p, q);
    if (left && right) return root;
    return left ? left : right;
};
```

---

## [diameter of binary tree](https://leetcode.com/problems/diameter-of-binary-tree/description/)

```
diameter updated at every node during dfs.
dfs return the max Number of nodes along on branch for each subtree.
diameter = max # of node along the left subtree + max #along the right subtree + 1 - 1.
```

```javascript
var diameterOfBinaryTree = function(root) {
    let diameter = 0;
    function dfs(node) {
        if (!node) return 0;
        let leftNodeNum = dfs(node.left),
            rightNodeNum = dfs(node.right);
        let nodeNum = 1 + leftNodeNum + rightNodeNum;
        diameter = Math.max(diameter, nodeNum - 1);
        return 1 + Math.max(leftNodeNum, rightNodeNum);
    }
    dfs(root);
    return diameter;
};
```

---

## [subtree of another tree](https://leetcode.com/problems/subtree-of-another-tree/description/)

> dfs from top down. for each node in s, if it's equal to root in t, then it's a potential match, use `isSame` to check two tree is the same. if not , resort to the left & right of the root in t.

```javascript
var isSubtree = function(s, t) {
    if (!s || !t) return !s && !t;
    if (s.val !== t.val) return isSubtree(s.left, t) || isSubtree(s.right, t);
    return isSame(s, t) || isSubtree(s.left, t) || isSubtree(s.right, t);
};

var isSame = function(s, t) {
    if (!s || !t) return !s && !t;
    return s.val === t.val && isSame(s.left, t.left) && isSame(s.right, t.right);
};
```

---

## [binary tree upside down](https://leetcode.com/problems/binary-tree-upside-down/description/)

1. buttom up transformation
the new root comes from the bottom recursion

```javascript
var upsideDownBinaryTree = function(root) {
    if (!root || !root.left) return root;
    let newRoot = upsideDownBinaryTree(root.left);
    let hook = root.left;
    hook.left = root.right;
    hook.right = root;
    root.left = root.right = null;
    return newRoot;
};
```
---

## [symmetric tree](https://leetcode.com/problems/symmetric-tree/description/)

> topdown comparison

```javascript
var isSymmetric = function(root) {
    if (!root) return true;
    return isSame(root.left, root.right);
};

function isSame(root1, root2) {
    if (!root1 || !root2) return !root1 && !root2;
    return root1.val === root2.val && isSame(root1.left, root2.right) && isSame(root1.right, root2.left);
}
```

---

## [max depth of binary tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)

```javascript
var maxDepth = function(root) {
    function dfs(node) {
        if (!node) return 0;
        return 1 + Math.max(dfs(node.left), dfs(node.right));
    }
    return dfs(root);
};
```

---

## [find leaves of binary tree](https://leetcode.com/problems/find-leaves-of-binary-tree/description/)

```javascript
var findLeaves = function(root) {
    let results = [];
    function getHeight(root) {
        if (!root) return -1;
        let height = 1 + Math.max(getHeight(root.left), getHeight(root.right));
        if (results[height] === undefined) {
            results[height] = [];
        }
        results[height].push(root.val);
        return height;
    }
    getHeight(root);
    return results;
};
```

---

## [find largest value in each tree row](https://leetcode.com/problems/find-largest-value-in-each-tree-row/description/)

```javascript
var largestValues = function(root) {
    let que = root ? [root] : [];
    let result = [];
    while (que.length > 0) {
        result.push(Math.max(...que.map(x => x.val)));
        let nextQue = [];
        for (let node of que) {
            if (node.left) nextQue.push(node.left);
            if (node.right) nextQue.push(node.right);
        }
        que = nextQue;
    }
    return result;
};
```

---

## [second minimum node in a binary tree](https://leetcode.com/problems/second-minimum-node-in-a-binary-tree/description/)

保留两个最小值，preorder
如果碰到和这两个最小值一样的数，记得跳过

```javascript
var findSecondMinimumValue = function(root) {
    let min = Infinity, secMin = Infinity;
    function preorder(node) {
        if (!node) return;
        if (node.val !== min && node.val !== secMin) {
            if (node.val < min) {
                secMin = min;
                min = node.val;
            } else if (node.val < secMin) {
                secMin = node.val;
            }
        }
        preorder(node.left);
        preorder(node.right);
    }

    preorder(root);

    return secMin == Infinity ? -1 : secMin;
};
```
