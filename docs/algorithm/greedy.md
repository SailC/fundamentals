## [task scheduler](https://leetcode.com/problems/task-scheduler/description/)
`有思路` `代码脏` `greedy` `math` `simulation`

![1](./images/1.png)
![2](./images/2.png)

1. priority que simulation
> 贪心： 尽可能调度cnt比较大的task，这样可以有效填充cooling period。如果调度cnt较小的task，那么会导致cnt较大的task积累，不利于分散task种类。尽可能保留多种task好互相interleave。
> 实现的时候注意不要把heap和array 的length size 搞混

2. math
> 尽可能用不同的task填充cooling window， 最后一个cooling window填不满也没有关系，但是之前的cooling window需要用idle tick填充，这样的cooling window的个数是由出现次数最多的task 决定的 `maxCnt - 1`. (每一个window只负责完成其中一个task).
> 所以最多出现多少个相同的task，就需要多少个window，能够撑到最后一个window的task，一定是出现次数最多的那几个。
> 填充的时候按照出现次数顺序排序，就能保证同样的task之间间隔为cooling window
> 特殊情况是不需要idle

```javascript
var leastInterval = function(tasks, n) {
    //construct que for the tasks to be executed
    let taskQue = new Heap((a, b) => b - a);
    let cntMap = new Map();
    for (let task of tasks) cntMap.set(task, (cntMap.get(task) || 0) + 1);
    for (let task of cntMap.keys()) taskQue.push(cntMap.get(task));

    let ticks = 0;
    while (taskQue.size > 0) {
        let nextQue = [];
        for (let cooling = 0; cooling <= n; cooling++) {
            if (taskQue.size > 0) {
                let taskNum = taskQue.pop();
                taskNum--;//process the task
                if (taskNum > 0) nextQue.push(taskNum);
            }
            ticks++;
            if (taskQue.size === 0 && nextQue.length === 0) break;
        }
        // taskQue = nextQue; bug1 heap !== array
        while (nextQue.length > 0) taskQue.push(nextQue.pop());
    }

    return ticks;
};

leastInterval = function(tasks, n) {
    let cnts = new Array(26).fill(0);
    for (let task of tasks) {
        let idx = task.charCodeAt(0) - 'A'.charCodeAt(0);
        cnts[idx]++;
    }
    let maxCnt = Math.max(...cnts);
    let sameFreqNum = cnts.filter(cnt => cnt === maxCnt).length;
    let result = (maxCnt - 1) * (n + 1) + sameFreqNum;
    return Math.max(result, tasks.length);
};
```

---

## [find celebrities](https://leetcode.com/problems/find-the-celebrity/description/)

`bruteforce`
> check every one, find out if he/she is celebrity or not.
`const isCeleb = x => knows(i, x) && !knows(x, i) for each i !== x`

`greedy`
> set candidate to 0, i from 1 to n, check if the current candidates knows i, if so, i becomes potential celebrity. after the iteration, check if the candidate is the celebrity.

> how did this apprach won't miss the celebrity ? if the celebrity exists, then it would be elected at some point by the current candidate. After the celebrity has been elected, it doesn't know anyone , so it will stay there until the scan finished.

```javascript
var solution = function(knows) {
    /**
     * @param {integer} n Total people
     * @return {integer} The celebrity
     */
    return function(n) {
        let candidate = 0;
        for (let i = 1; i < n; i++) {
            if (i !== candidate && knows(candidate, i)) candidate = i;
        }
        for (let i = 0; i < n; i++) {
            if (i === candidate) continue;
            const isCeleb = (candidate, i) => knows(i, candidate) && !knows(candidate, i);
            if (!isCeleb(candidate, i)) return -1;
        }
        return candidate;
    };
};
```

## [minimum number of arrows to burst](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/description/)

every ballon needs a arrow to busrt. always shoot the arrow at the end pos for the current ballon because the incoming ballons are all ended to the right of the pos.

`why not sort by start` ?
because we can't make sure the incoming ballons ended to the right of the pos , the arrow may miss the target if the incoming ballons ends before the pos. we still have to use greedy , but it's not correct this time.

```javascript
var findMinArrowShots = function(points) {
    let arrows = 0;
    points.sort(([s1, e1], [s2, e2]) => e1 - e2);
    while (points.length > 0) {
        let pos = points.shift()[1]; //shot an arrow at the end of the ballon
        arrows++;
        // burst as many as ballons as possible
        const inRange = ([start, end]) => (pos >= start && pos <= end);
        while (points.length > 0 && inRange(points[0])) points.shift();
    }
    return arrows;
};
```

---

## [can place flowers](https://leetcode.com/problems/can-place-flowers/description/)

新增 n 盆花，和现有的花一起两两不间隔
如果发现一个槽两遍都没有花，就可以种花

理由是，维持一个不变量， 之前扫过的区间都是符合两两不间隔的条件。如果这个槽中了，不影响之前的不变量，只影响 x + 1这个槽能不能种花。如果选择不中x槽，而中x + 1槽，有两种情况
首先x + 1槽不一定能种花，这样x槽就白白浪费了
其次就算x + 1槽可以种花，也只是和x槽持平，而且x + 1槽还影响了x + 2

```javascript
var canPlaceFlowers = function(flowerbed, n) {
    let cnt = 0;
    for (let i = 0; i < flowerbed.length && cnt <= n; i++) {
        let prev = i === 0 ? 0 : flowerbed[i - 1];
        let next = i === flowerbed.length - 1 ? 0 : flowerbed[i + 1];
        if (flowerbed[i] === 0 && prev === 0 && next === 0) {
            flowerbed[i] = 1;
            cnt++;
        }
    }
    return cnt >= n;
};
```
