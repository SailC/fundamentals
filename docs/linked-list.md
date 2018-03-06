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
