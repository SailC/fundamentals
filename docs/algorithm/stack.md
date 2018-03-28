# Stack

## [valid parenthesis](https://leetcode.com/problems/valid-parentheses/description/)

1. stack
> scan the input string from left to right.
> if the next char is left paren, push it to the stack.
> we maintain a invariant that the stack only contains the left parens, all the right parens will be cancelled out by the closest matching left parens.
> So, if it's a right parent, it checks the closest left parens, which should be on the top of the stack. if it doesn't match return false, otherwise, cancel the parens.
> finally check if all the left parens have been cancelled out.

```javascript
var isValid = function(s) {
    const isMatch = (a, b) => new Set(['()', '{}', '[]']).has(`${a}${b}`);
    const isLeft = c => new Set(['(', '{', '[']).has(c);
    let stack = [];
    for (let c of s) {
        if (isLeft(c)) {
            stack.push(c);
        } else {
            if (stack.length === 0 || !isMatch(stack.pop(), c)) return false;
        }
    }
    return stack.length === 0;
};
```
---
## [flatten nested list iterator](https://leetcode.com/problems/flatten-nested-list-iterator/description/)

1. Flatten the nested List on demand
First think of how we recursively flatten the nested List
- we keep pushing nested integers to the stack until we find the first non-list integer
- unlike recursion, we can't mantain the pointers to which nested integer we're visiting , so we put all the nested integer into the stack at once. we want to iterate from left to right, so we need to push into the stack in reverse fashion.
Notice that:
nested Integer can be empty list, in which case the stack is not empty. you need to flatten the list in order to verify if we have next;

```javascript
var NestedIterator = function(nestedList) {
    this.stack = nestedList.reverse();
};

NestedIterator.prototype.hasNext = function() {
    //bug1: return this.tack.length > 0
    const peek = () => this.stack[this.stack.length - 1];
    while (this.stack.length > 0 && !peek().isInteger()) {
        let top = this.stack.pop();
        for (let nestedInt of top.getList().reverse()) {
            this.stack.push(nestedInt);
        }
    }
    return this.stack.length > 0 ;
};

NestedIterator.prototype.next = function() {
    return this.stack.pop().getInteger();
};

```
---
## [flatten 2d vector](https://leetcode.com/problems/flatten-2d-vector/description/)

```javascript
var Vector2D = function(vec2d) {
    this.stack = vec2d.reverse();
};

Vector2D.prototype.hasNext = function() {
    while (this.stack.length > 0 && typeof(this.stack[this.stack.length - 1]) !== 'number') {
        for (let x of this.stack.pop().reverse()) this.stack.push(x);
    }
    return this.stack.length > 0;
};

Vector2D.prototype.next = function() {
    return this.stack.pop();
};
```
---
## [Binary Search Tree Iterator](https://leetcode.com/problems/binary-search-tree-iterator/description/)

`一遍过` `BST` `In order traversal` `stack`

1. in order traversal
> `next smallest number in BST` => `in order traversal`
> This is a application of the iterative inorder traversal. we need to make sure the next element poping from the stack is the next smallest one. which means all the previous smaller ones have all been processed.
> So for each newly process ones, we make sure the left branch has all been processed, and push the right subtree's left branch to the stack.

```javascript
var BSTIterator = function(root) {
    this.stack = [];
    for (let node = root; node; node = node.left) this.stack.push(node);
};


/**
 * @this BSTIterator
 * @returns {boolean} - whether we have a next smallest number
 */
BSTIterator.prototype.hasNext = function() {
    return this.stack.length > 0;
};

/**
 * @this BSTIterator
 * @returns {number} - the next smallest number
 */
BSTIterator.prototype.next = function() {
    let node = this.stack.pop();
    for (let cur = node.right; cur; cur = cur.left) this.stack.push(cur);
    return node.val;
};
```

---
## [Zigzag Iterator](https://leetcode.com/problems/zigzag-iterator/description/)
`有思路` `iterator` `que`

1. index + buffer
> we use an index i to indicate the next row idx, and stores the col id for each row. each time we check if the col id is valid, if not we continue to the next row.

2. que + iterator
> Uses a que to store the iterators in different vectors. Every time we call next(), we pop an element from the list, and re-add the iterator to the end to cycle through the lists.

```javascript
var ZigzagIterator = function ZigzagIterator(v1, v2) {
    this.k = 2;
    this.i = 0;
    this.js = new Array(this.k).fill(0);
    this.vs = [v1, v2];
    this.n = v1.length + v2.length;
    this.cnt = 0;
};

ZigzagIterator.prototype.hasNext = function hasNext() {
    return this.cnt < this.n;
};

ZigzagIterator.prototype.next = function next() {
    let [k, i, js, vs] = [this.k, this.i, this.js, this.vs];
    while (js[i] === vs[i].length) i = (i + 1) % k;
    this.i = i;
    let idx = js[i]++;
    this.cnt++;
    this.i = (this.i + 1) % k;
    return vs[i][idx];
};

var ZigzagIterator = function ZigzagIterator(v1, v2) {
    this.iterators = [v1, v2].map(x => x[Symbol.iterator]());
    this.n = v1.length + v2.length;
    this.cnt = 0;
};

ZigzagIterator.prototype.hasNext = function hasNext() {
    return this.cnt < this.n;
};

ZigzagIterator.prototype.next = function next() {
    let its = this.iterators;
    while (true) {
        let it = its.shift();
        let next = it.next();
        if (!next.done) {
            its.push(it);
            this.cnt++;
            return next.value;
        }
    }
};

var ZigzagIterator = function ZigzagIterator(v1, v2) {
    this.list = [];
    for (let v of [v1, v2]) this.list.push(v[Symbol.iterator]());
    this.nextVal = null;
};

ZigzagIterator.prototype.hasNext = function hasNext() {
    while (this.list.length > 0) {
        let it = this.list.shift();
        let next = it.next();
        if (!next.done) {
            this.nextVal = next.value;
            this.list.push(it);
            return true;
        }
    }
    return false;
};

ZigzagIterator.prototype.next = function next() {
    return this.nextVal;
};
```
---
## [simplify path](https://leetcode.com/problems/simplify-path/description/)

> 字符串tokenize很麻烦，用split加filter过滤掉special case
> 然后main loop就很简单了

```javascript
var simplifyPath = function(path) {
    let tokens = path.split('/').filter(x => x !== '');
    let stack = [];
    for (let token of tokens) {
        if (token === '.') continue;
        if (token === '..') {
            if (stack.length > 0) stack.pop();
        } else {
            stack.push(token);
        }
    }
    return '/' + stack.join('/');
};
```
---
## [exclusive time of functions](https://leetcode.com/problems/exclusive-time-of-functions/description/)

1. `stack simulation`
> Scan the log from top to bottom. For each line of log:
> 1) if it's a start, it's either the first process or interrupting the previous process. Both case require the process to be pushed to the stack, we need to store the pID and startTime for later calculation of the time span. If it's interrupting, we need to calculate the previous timeSpan before interuption. (don't pop the previous process as it's going to continue executing after the current process finishes)
> 2) if it's a end, calculate the current time span of the current process and pop the stack to return to the original process. A tricky part is to update the previous process start time so that it won't count the overlapping time span.

```javascript
var exclusiveTime = function(n, logs) {
    let result = new Array(n).fill(0);
    let stack = []; // store list of numbers
    for (let line of logs) {
        // bug0: let [fId, action, time] = logs.split(':');
        let [fId, action, time] = line.split(':');
        // bug1: forget to convert time to Number
        time = Number(time);
        if (action === 'start') {
            if (stack.length > 0) {
                let [lastId, _, lastTime] = stack[stack.length - 1];
                result[lastId] += time - lastTime;
            }
            stack.push([Number(fId), action, Number(time)]);
        } else {
            let [curId, _, startTime] = stack.pop();
            result[curId] += time - startTime + 1;
            if (stack.length > 0) {
                stack[stack.length - 1][2] = time + 1;
            }
        }
    }
    return result;
};
```

---

## [largest rectangle in histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)

```
- 每遍历一个element，就有可能开启一个新的rect。将这种可能性的起点存在pStack里面，hStack用来记录这个rect的高度
- 当新的element比栈顶元素高的时候，可能性保持，入栈。
- 如果矮，那么pop出那些可能性破灭的元素，计算maxVal。
- 如果一样高，只用关心之前入栈的可能性就行，所以不用push。
- 在栈尾添加一个-1来消除特殊情况.

figure out the `starting position` and `ending position` of each incomming element bar.
1) `if (stack.length === 0 || barHeight > top)` the `starting position` is current index since left bars are all shorter. `ending pos` we don't know yet, resort to future incoming bars
2) `else if barHeight === top`, we ignore this case since we can count on the previous bar and its ending pos
3) `else if barHeight < top`, for the bar on the top of the stack, it's starting pos is stored in the stack, it's `ending pos` is the current index, so pop it and calc its area. Continue this process until `barHeight >= top`, now we can push the incoming bar to the stack.
but ... this incoming bar starting from the pos of the last poped top.

`edge case`
`[2,1,2]` , when the `1` is pushed to the stack, the `starting position` of `1` is actually the index of the last poped `2`. Because to the left of `2` are all elements smaller than `1` so `1` can't start there.
```

```javascript
var largestRectangleArea = function(heights) {
    heights.push(0);
    let maxArea = 0, stack = [];
    for (let i = 0; i < heights.length; i++) {
        let h = heights[i];
        let s = i;
        while (stack.length > 0 && h < stack[stack.length - 1][1]) {
            let [start, height] = stack.pop();
            s = start;
            maxArea = Math.max(maxArea, height * (i - start));
        }
        stack.push([s, h]);
    }
    return maxArea;
};
```

---

## [evaluate reverse polish notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/description/)

basic stack opr
`const isDigit = token => /[0-9]+/.test(token);`  although it's not strict, by sufficient to tell the digit in this case. digit can start with `-`

```javascript
var evalRPN = function(tokens) {
    let stack = [];
    for (let token of tokens) {
        if (new Set(['+', '-', '*', '/']).has(token)) {
            let num2 = stack.pop(), num1 = stack.pop();
            switch (token) {
                case '+':
                    stack.push(num1 + num2);
                    break;
                case '-':
                    stack.push(num1 - num2);
                    break;
                case '*':
                    stack.push(num1 * num2);
                    break;
                case '/':
                    stack.push(~~(num1 / num2));
                    break;
                default:
                    throw 'unsupported opr';
            }
        } else stack.push(Number(token));
    }
    return stack.pop();
};
```

---

## [max stack](https://leetcode.com/problems/max-stack/description/)

push和popMax操作不可能都是O(1) 否则，使用这个操作就可以实现O(n) 的sort
push为O(1) ， 那么popmax最多为O(logn)

实现为O(n) 和minstack一样维护一个记录着max idx的stack，每次popmax的时候都找到idx釜底抽薪，然后重新构建maxStack

https://discuss.leetcode.com/topic/110018/java-accepted-with-one-stack-and-one-pq O(log) push O(n) pop

用linked list加heap可以做到 push O(lgn), pop O(n) popMax(lgn)

```javascript
/**
 * initialize your data structure here.
 */
var MaxStack = function() {
    this.stack = [];
    this.maxStack = [];
};

/**
 * @param {number} x
 * @return {void}
 */
MaxStack.prototype.push = function(x) {
    this.stack.push(x);
    if (this.maxStack.length === 0) {
        this.maxStack.push(0);
    } else {
        let idx = this.maxStack[this.maxStack.length - 1];
        if (x >= this.stack[idx]) {
            this.maxStack.push(this.stack.length - 1);
        } else {
            this.maxStack.push(idx);
        }
    }
};

/**
 * @return {number}
 */
MaxStack.prototype.pop = function() {
    this.maxStack.pop();
    return this.stack.pop();
};

/**
 * @return {number}
 */
MaxStack.prototype.top = function() {
    return this.stack[this.stack.length - 1];
};

/**
 * @return {number}
 */
MaxStack.prototype.peekMax = function() {
    let idx = this.maxStack[this.maxStack.length - 1];
    return this.stack[idx];
};

/**
 * @return {number}
 */
MaxStack.prototype.popMax = function() {
    let idx = this.maxStack[this.maxStack.length - 1];
    let result = this.stack[idx];
    this.stack.splice(idx, 1);
    this.maxStack = [];
    let localMax;
    for (let i = 0; i < this.stack.length; i++) {
        if (i === 0 || this.stack[i] >= localMax) {
            localMax = this.stack[i];
            this.maxStack.push(i);
        } else {
            this.maxStack.push(this.maxStack[this.maxStack.length - 1]);
        }
    }
    return result;
};

```
