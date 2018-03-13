## [split linked list in parts](https://leetcode.com/problems/split-linked-list-in-parts/description/)

`有思路` `round robin` `partition`

> 最初想先用round robin算出groupSize，然后再遍历链表
> 后来发现前r个group的size = 商 + 1, 就无需提前算出groupSize了
> Time: O(N) 链表长度

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/725-ep106-1.png)

```javascript
var splitListToParts = function(root, k) {
    let length = getListLength(root);
    let partSize = ~~(length / k), restSize = length % k;
    let parts = [];
    let cur = root, prev = null;
    for (let i = 0; i < k; i++) {
        //create each part
        parts[i] = cur;
        let size = partSize + (restSize > 0 ? 1 : 0);
        for (let j = 0; j < size; j++) {
            prev = cur;
            cur = cur.next;
        }
        if (prev) prev.next = null;
        restSize--;
    }
    return parts;
};
```
---
## [flatten binary tree to linked list](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/description/)

> 好题目，考察对preorder traversal的应用。链表其实就是tree的preorder traversal， 所以只要在preorder的过程中记住prev node，然后将prev 和cur node链接起来，
> 注意链接的过程会改变父节点的结构，所以记得save left and right children before modify inplace. And recurse via left & right.

```javascript
var flatten = function(root) {
    let prev = null;
    function preOrder(node) {
        if (!node) return;
        let [left, right] = [node.left, node.right];
        if (prev) [prev.left, prev.right] = [null, node];
        prev = node;
        preOrder(left);
        preOrder(right);
    }
    preOrder(root);
};
```
---
## flatten binary search tree to sorted circular doubly linked list

> bst sorted => inorder traversal, 用 prev 指针记录前一个traverse的node进行连接
> 由于要返回head已经要做成circular，我们需要用dummy node来记录head位置，并做最后的链接

```javascript
function treeToDoublyList(root) {
    if (!root) return null;
    let head = new TreeNode();// dummy
    let prev = head; //eliminate edge case
    function inOrder(node) {
        if (!node) return;
        let [left, right] = [node.left, node.right]; //save info
        inOrder(left);
        [prev.right, node.left] = [node, prev]; //link
        prev = node; //update prev
        inOrder(right);
    }
    inOrder(root);
    prev.right = head.right; //link tail to head
    head.right.left = prev; //link head to tail
    return head.right; //return start
}
```
---
## [reverse linked list](https://leetcode.com/problems/reverse-linked-list/description/)

1. `iterative`
> 和flatten binary tree一样，都是traverse的过程中保留前面一个和后面一个节点的信息，然后一路进行连接和更新。
2. `recursive`
> special case: when list only has less than 2 nodes, no need to reverse
> assume the right part is already reversed, two more clean ups:
1) conect the tail of the reversed list to the original head
2) set head.next to null to avoid loop

```javascript
var reverseList = function(head) {
    let prev = null, cur = head, next = head.next;
    while (cur) {
        next = cur.next;
        cur.next = prev;
        prev = cur;
        cur = next;
    }
    return prev;
};

var reverseList = function(head) {
    if (!head || !head.next) return head;
    let newHead = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    return newHead;
}
```
---
## [palindrom linked list](https://leetcode.com/problems/palindrome-linked-list/description/)

1. recursion
> post order recursion will touch the last element first
> each time last elment is touched , increment the start node by one step

2. iterative
> fast + slow to find second half of palindrome
> reverse the second half of the linked list
> see if first half & second half are the same

```javascript
var isPalindrome = function(head) {
    let start = head;
    const dfs = node => {
        if (node === null) {
            return true;
        }
        if (dfs(node.next) && (node.val === start.val)) {
            start = start.next;
            return true;
        }
        return false;
    };
    return dfs(head);
};

isPalindrome = function(head) {
    if (!head || !head.next) return true;
    let slow = head, fast = head;
    while (fast && fast.next) {
        fast = fast.next.next;
        slow = slow.next;
    }
    if (fast) slow = slow.next;
    slow = reverse(slow);
    while (slow) {
        if (head.val !== slow.val) return false;
        [head, slow] = [head.next, slow.next];
    }
    return true;
};

function reverse(head) {
    let prev = null, cur = head;
    while (cur) {
        let next = cur.next;
        cur.next = prev;
        prev = cur;
        cur = next;
    }
    return prev;
}
```
---
## [swap nodes in pairs](https://leetcode.com/problems/swap-nodes-in-pairs/description/)

`recursion`
> much cleaner than the iterative approach.
1) swap the first two nodes if possible
2) recurse the rest of the list
3) link them

`iterative`
> keep track of first and second node & link them
> tricky part: before go to the next pair, need to link first with the second of the next pair (the second pair hasn't been updated like recursion)
> this approach doens't scale to k group, because it's harder to keep track of k pointers.

```javascript
var swapPairs = function(head) {
    if (!head || !head.next) return head;
    let [first, second] = [head, head.next];
    let next = swapPairs(second.next);
    first.next = next;
    second.next = first;
    return second;
};

swapPairs = function(head) {
    if (!head || !head.next) return head;
    let [first, second] = [head, head.next];
    head = second;
    while (first && second) {
        let next = second.next;
        second.next = first;
        if (next && next.next) first.next = next.next;
        else first.next = next;
        first = next;
        second = first ? first.next : null;
    }
    return head;
};
```
---
## [reverse nodes in k group](https://leetcode.com/problems/reverse-nodes-in-k-group/description/)

1. recursion
> 先check edge case，看看有没有足够多的node来reverse，如果剩下的node少于k个，leave them alone
> reverse the rest of the list with reverseKGroup and use the head as the prev.
> link first half with rest

```javascript
var reverseKGroup = function(head, k) {
    let n = 0;
    for (let cur = head; cur; cur = cur.next) n++;
    if (k === 1 || n < k) return head;
    let prev = null, cur = head;
    for (let i = 0; cur && i < k; i++) {
        let next = cur.next;
        cur.next = prev;
        prev = cur;
        cur = next;
    }
    head.next = reverseKGroup(cur, k);
    return prev;
};
```
---
## [merge k sorted lists](https://leetcode.com/problems/merge-k-sorted-lists/description/)

1. `Merge one by one`
> say every list has length of n
> total # of nodes to merge = 2n + 3n + 4n + ... kn = O(nk^2)

2. `heap`
> Use a minHeap of size k which stores the head node of each list. the next node to merge is the top of the
heap.
> time: O(kn * logk) = O(nklgk)

3. `divide & conquer`
> bruteforce merge touchs the first list k times, we don't need to do that. We can only touch each list lgk times.
> we merget two list into one at each round. after lgk round, we will have one list.
> time : each round we touches nk nodes, so T = O(nklgk)

```javascript
var mergeKLists = function(lists) {
    let minHeap = new Heap((a, b) => a.val - b.val);
    for (let list of lists) {
        //bug1 forget to check list is null
        if (list) minHeap.push(list);
    }
    let head = new ListNode();
    let node = head;
    while (minHeap.size > 0) {
        let list = minHeap.pop();
        node.next = list;
        // bug2 forget to check list is null
        if (list.next) minHeap.push(list.next);
        node = node.next;
    }
    return head.next;
};

var mergeKLists = function(lists) {
    while (lists.length > 1) {
        let merged = [];
        for (let i = 0; i < lists.length; i += 2) {
            let list = i === lists.length - 1 ? lists[i] : merge(lists[i], lists[i + 1]);
            merged.push(list);
        }
        lists = merged;
    }
    return lists.length === 0 ? null: lists[0];
};

function merge(listA, listB) {
    let head = new ListNode();
    let node = head;
    while (listA && listB) {
        if (listA.val < listB.val) {
            node.next = listA;
            listA = listA.next;
        } else {
            node.next = listB;
            listB = listB.next;
        }
        node = node.next;
    }
    node.next = listA ? listA : listB;
    return head.next;
}
```
