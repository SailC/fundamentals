## [my calendar I](https://leetcode.com/problems/my-calendar-i/description/)

`有思路` `不熟练` `bst`

1. brute force
> When booking a new event [start, end), check if every current event conflicts with the new event. If none of them do, we can book the event.
> Time: O(n) book
2. balanced tree
> If we maintained our events in sorted order, we could check whether an event could be booked in O(logN) time. We need a data structure that keeps elements sorted and supports fast insertion.
> Time: O(logN) on randome data, O(N) worst
> 要logN时间插入，heap可以做到，但是heap无法支持二分搜索。array可以支持二分，但是无法支持logN时间插入。
> 二分查找的过程一旦出现overlap马上return false.

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/729-ep112.png)

```javascript
var MyCalendar = function() {
    this.events = [];
};

MyCalendar.prototype.book = function(start, end) {
    const conflict = (a, b) => !(a[0] >= b[1] || a[1] <= b[0]);
    let event = [start, end];
    for (let e of this.events) {
        if (conflict(e, event)) return false;
    }
    this.events.push(event);
    return true;
};

class TreeNode {
    constructor(start, end) {
        this.start = start;
        this.end = end;
        this.left = this.right = null;
    }
}

var MyCalendar = function() {
    this.root = null;
};

MyCalendar.prototype.book = function(start, end) {
    if (!this.root) {
        this.root = new TreeNode(start, end);
        return true;
    }
    let root = this.root, node = new TreeNode(start, end);
    while (root) {
        if (start >= root.end) {
            if (!root.right) {
                root.right = node;
                return true;
            }
            root = root.right;
        } else if (end <= root.start) {
            if (!root.left) {
                root.left = node;
                return true;
            }
            root = root.left;
        } else {
            return false;
        }
    }
};
```
---
## [valid binary search tree](https://leetcode.com/problems/validate-binary-search-tree/description/)

`一遍过` `inorder` `top down` `bottom up`

1. `top down`
> enforcing min max rule all the way to the bottom

2. `bottom up`
> return min and max of each subtree and validate the root.

3. `in order traversal`
> in order traversal should see monotonically increasing seq.

```javascript
var isValidBST = function(root) {
    return isBST(root, -Infinity, Infinity);
};

function isBST(root, min, max) {
    if (!root) return true;
    return root.val > min && root.val < max && isBST(root.left, min, root.val) && isBST(root.right, root.val, max);
}

isValidBST = function(root) {
    let prev = null;
    function inOrder(node) {
        if (!node) return true;
        if (!inOrder(node.left)) return false;
        if (prev && node.val <= prev.val) return false;
        prev = node;
        return inOrder(node.right);
    }
    return inOrder(root);
};
```

---
## [serialize and deserialize bst](https://leetcode.com/problems/serialize-and-deserialize-bst/description/)

`有思路` `不熟` `topdown recursion`

> The special property of binary search trees compared to general binary trees allows a more compact encoding. So while the solutions to problem #297 still work here as well, they're not as good as they should be.
> also use `preorder` to dfs encode the string.
when `decode`, leverage the bst property to figure out the left and right subtree's corresponding values.
1. bottom up
> when deserialize, find the separator in O(n) time and recurse on left & right
> time: O(N ^ 2) <- T(N) = T(N - 1) + O(N) in the worst case (linked list tree)
2. top down
> when deserialize, check if the current subtree can consume the next data as its root by checking the boundaries in O(1)
> time: O(N) each node is visited exactly once.

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/449-ep91.png)

```javascript
var serialize = function(root) {
    let output = [];
    function preOrder(node) {
        if (!node) return;
        output.push(node.val);
        preOrder(node.left);
        preOrder(node.right);
    }
    preOrder(root);
    return output.join(',');
};

var deserialize = function(data) {
    if (data === '') return null;//bug ''.split(',') === ['']
    let input = data.split(',').map(x => Number(x));
    function buildTree(lo, hi) {
        if (lo > hi) return null;
        let root = new TreeNode(input[lo]);
        let i = lo + 1;
        while (input[i] < input[lo] && i <= hi) i++;
        // i > hi || input[i] > i
        root.left = buildTree(lo + 1, i - 1);
        root.right = buildTree(i, hi);
        return root;
    }
    return buildTree(0, input.length - 1);
};

deserialize = function(data) {
    if (data === '') return null;//bug ''.split(',') === ['']
    let input = data.split(',').map(x => Number(x));
    let i = 0, n = input.length;
    function buildTree(min, max) {
        if (i === n) return null;
        if (input[i] <= min || input[i] >= max) return null;
        let root = new TreeNode(input[i++]);
        root.left = buildTree(min, root.val);
        root.right = buildTree(root.val, max);
        return root;
    }
    return buildTree(-Infinity, Infinity);
};
```
---
