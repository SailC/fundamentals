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
