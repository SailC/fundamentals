## [my calendar I](https://leetcode.com/problems/my-calendar-i/description/)
`有思路` `不熟练` `bst`

1. brute force
> When booking a new event [start, end), check if every current event conflicts with the new event. If none of them do, we can book the event.
> Time: O(n) book
2. balanced tree
> If we maintained our events in sorted order, we could check whether an event could be booked in O(\log N)O(logN) time. We need a data structure that keeps elements sorted and supports fast insertion.
> Time: O(logN) on randome data, O(N) worst
> 要logN时间插入，heap可以做到，但是heap无法支持二分搜索。array可以支持二分，但是无法支持logN时间插入。
> 二分查找的过程一旦出现overlap马上return false.

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
