- [trial & fail](https://leetcode.com/problems/k-th-smallest-prime-fraction/discuss/115819/Summary-of-solutions-for-problems-%22reducible%22-to-LeetCode-378)
---
## [Kth Smallest Element in a Sorted Matrix](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/description/)

1. Heap
> 这题看上去很像merge K sorted list, 先将 min(n, k)个最小元素放入一个minHeap，每次从minHeap中pop出来一个元素之后，就将其后续的元素也放入minHeap，这样做保证当前最小的几个元素都在heap中，也保证了下一个出来的元素就是接下来的最小元素。
> 时间复杂度 `O(max(N, K) + KlgN)`

2. 二分查找
> **如果一个数组是有序的话，我们可以通过对index进行二分 （好处是index 约等于cnt，你可以在O(1)时间内知道左边有多少个元素）
如果一个数组是无序的话，我们只能通过对value进行二分**
> 这一题二维数组不是蛇形有序，所以不能通过对下标进行编码成一维数组然后对index进行二分。
> `kth smallest element === find a value x so that f(x) = true `  predicate `f(x) =  there are at least k elements in the matrix whose value <= x` . and `if f(x) = true, for all y > x, f(y) = true` , `if f(x) = false, for all y < x, f(y) = false`
> so our goal is to find the first x so that `f(x) = true`
所以问题就变成如何在尽可能短的时间算出 `the number of elements in matrix whose value <= x`
> 最傻逼的做法就是遍历一遍矩阵，用 `O(n^2)` 求出.
> 聪明一点的做法是遍历每一行，然后利用每一行单调递增的属性进行二分查找，找出第一个比x 大的元素的index就是cnt了，耗时 `O(nlogn)`
> 更巧妙的， 利用matrix在每一行，每一列单调递增的特点，遍历每一行，初始列指针为最靠右，如果当前元素比x大的话，那么下面几行同列的元素一定比x大，所以j就可以放心前移，知道移动到 <= x 的位置。
> 这里 i 和 j 都是移动了n下，所以复杂度是O(n)
> 整个复杂度是 `O(n lg (max - min))`

```javascript
var kthSmallest = function(matrix, k) {
    if (matrix === null || matrix.length === 0) return;
    let n = matrix.length;
    let lo = matrix[0][0], hi = matrix[n - 1][n - 1];

    const cntLessEqual = target => {
        let j = n - 1, cnt = 0;
        for (let i = 0; i < n; i++) {
            while (j >= 0 && matrix[i][j] > target) j--;
            cnt += j + 1;
        }
        return cnt;
    };

    while (lo < hi) {
        let mid = lo + ~~((hi - lo) / 2);
        if (cntLessEqual(mid) >= k) hi = mid;
        else lo = mid + 1;
    }
    //assume k is always valid
    return lo;
};

var kthSmallest = function(matrix, k) {
    if (matrix === null || matrix.length === 0) return;
    //Heap Node <val, row, col>
    let minHeap = new Heap((a, b) => a[0] - b[0]);
    let m = matrix.length, n = matrix[0].length;
    for (let i = 0; i < m; i++) minHeap.push([matrix[i][0], i, 0]);
    while (k > 0 && minHeap.size > 0) {
        let [val, row, col] = minHeap.pop();
        if (--k === 0) return val;
        if (col < n - 1) minHeap.push([matrix[row][col + 1], row, col + 1]);
    }
};
```

---
## [Find K Pairs with Smallest Sums](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/)

1. Brute force
> Just produce all pairs, sort them by sum, and return the first k.
2. Heap
> for example for nums1=[1,7,11], and nums2=[2,4,6]:
```
      2   4   6
   +------------
 1 |  3   5   7
 7 |  9  11  13
11 | 13  15  17
```
> We can keep a “horizon” of possible candidates, implemented as a heap / priority-queue, and roughly speaking we’ll grow from the top left corner towards the right/bottom.
> 我的做法是一开始只放左上角的一个元素进heap，之后每次pop都考虑移动nums1 & nums2两根指针。这样做的好处是heapSize比较小，每次pop操作size加一，最多k此操作，size最多是k。不好的地方是需要判重，因为对于同一个pair有可能出现不同的路径到达（可以向右或向下）。所以需要visited set来判重，
> 标准做法是一开始就往minHeap里面塞m个pair，<nums1[i], nums2[0]>, 然后每次pop，只需要移动nums的指针（只能向右走），加入一个新节点，因为限制了前进方向，所以不需要担心重复问题

```javascript
class Node {
    constructor(idx1, val1, idx2, val2) {
        this.idx1 = idx1;
        this.idx2 = idx2;
        this.val1 = val1;
        this.val2 = val2;
    }
}

var kSmallestPairs = function(nums1, nums2, k) {
    let m = nums1.length, n = nums2.length;
    let pairs = [];
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            pairs.push([nums1[i], nums2[j]]);
        }
    }
    return pairs.sort((a, b) => a[0] + a[1] - b[0] - b[1]).slice(0, k);
};

kSmallestPairs = function(nums1, nums2, k) {
    let m = nums1.length, n = nums2.length;
    let minHeap = new Heap((a, b) => a.val1 + a.val2 - b.val1 - b.val2);
    if (m === 0 || n === 0) return [];
    minHeap.push(new Node(0, nums1[0], 0, nums2[0]));
    let result = [];
    let visited = new Set();
    while (k > 0 && minHeap.size > 0) {
        let node = minHeap.pop();
        let key = `${node.idx1}:${node.idx2}`;
        if (!visited.has(key)) {
            result.push([node.val1, node.val2]);
            k--;
            if (node.idx1 < m - 1) minHeap.push(new Node(node.idx1 + 1, nums1[node.idx1 + 1], node.idx2, node.val2));
            if (node.idx2 < n - 1) minHeap.push(new Node(node.idx1, node.val1, node.idx2 + 1, nums2[node.idx2 + 1]));
        }
        visited.add(key);
    }
    return result;
};

kSmallestPairs = function(nums1, nums2, k) {
    let m = nums1.length, n = nums2.length;
    let minHeap = new Heap((a, b) => a[2] - b[2]);
    if (m === 0 || n === 0) return [];

    for (let i = 0; i < m; i++) {
        minHeap.push([i, 0, nums1[i] + nums2[0]]);
    }

    let result = [];
    while (k > 0 && minHeap.size > 0) {
        let [r, c, val] = minHeap.pop();
        result.push([nums1[r], nums2[c]]);
        if (c < n - 1) minHeap.push([r, c + 1, nums1[r] + nums2[c + 1]]);
        k--;

    }
    return result;
};
```

---
## [Kth Smallest Number in Multiplication Table](https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/description/)
---

> 为什么candidate 一定最后会落在matrix里面的一个元素上呢?
> 首先第K大一定是在matrix里面的一个元素，如果K合法的话
> 那么假设candidate比真正解小，那么小于等于candidate的元素一定少于K，`lo = mid + 1`, 一直右移
> 如果candidate比K真正解大，那么小于等于candidate的元素一定大于K，`hi = mid`，会一直左移
> 综上，一定会移动到candidate.

```javascript
var findKthNumber = function(m, n, k) {
    let A = Array.from(new Array(m).keys()).map(x => x + 1);
    let B = Array.from(new Array(n).keys()).map(x => x + 1);
    let minHeap = new Heap((a, b) => a[2] - b[2]);
    for (let i = 0; i < m; i++) minHeap.push([i, 0, A[i] * B[0]]);
    let ans;
    while (minHeap.size > 0 && k > 0) {
        let [r, c, val] = minHeap.pop();
        ans = val;
        k--;
        if (c < n - 1) minHeap.push([r, c + 1, A[r] * B[c + 1]]);
    }
    return ans;
};

findKthNumber = function(m, n, k) {
    let A = Array.from(new Array(m).keys()).map(x => x + 1);
    let B = Array.from(new Array(n).keys()).map(x => x + 1);

    function cntLessEq(target) {
        let j = n - 1, cnt = 0;
        for (let i = 0; i < m; i++) {
            while (j >= 0 && A[i] * B[j] > target) j--;
            cnt += j + 1;
        }
        return cnt;
    }

    let lo = A[0] * B[0], hi = A[m - 1] * B[n - 1];
    while (lo < hi) {
        let mid = lo + ~~((hi - lo) / 2);
        if (cntLessEq(mid) < k) lo = mid + 1;
        else hi = mid;
    }
    return lo;
};
```

## [Find K-th Smallest Pair Distance](https://leetcode.com/problems/find-k-th-smallest-pair-distance/description/)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/719-ep99-1.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/719-ep99-2.png)

0. Heap O(klgN + NlgN)
> Sort the points. For every point with index i, the pairs with indexes (i, j) [by order of distance] are (i, i+1), (i, i+2), ..., (i, N-1).
Let's keep a heap of pairs, initially heap = [(i, i+1) for all i], and ordered by distance (the distance of (i, j) is nums[j] - nums[i].) Whenever we use a pair (i, x) from our heap, we will add (i, x+1) to our heap when appropriate.

1. bruteforce  O(N^2)
> listing all the pairs and find the kth smallest by bucket sort or quick select.
2. binary search  (NlgN + N)
> find kth smallest pair distance === find a pair distance d > so that there are at least k pairs whose distance <= d.
> So the problem is reduce to
> given a distance d, how to find the number of pairs > whose distance is smaller than d.
> we can do this by scanning the array just once using sliding window whose rule is
`nums[r] - nums[l] <= d`. a valid window can give us some pairs that has pair distance <= d.
> we can also use dp to cnt the pairs. For a given right element, try to find the index of the left most element so that  `nums[l] >= nums[r] - dist` , which is equal to the number of elements that's smaller than `nums[r] - dist`.
we can calculate that lessThan array by dp.

```javascript
var smallestDistancePair = function(nums, k) {
    const MAX_DIFF = 1000000;
    // step1: compute the freq of all pairs
    let n = nums.length;
    let cnts = new Array(MAX_DIFF).fill(0);
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            let diff = Math.abs(nums[i] - nums[j]);
            cnts[diff]++;
        }
    }
    // step2: count sort and find kth smallest
    for (let cnt = 0, i = 0; i < MAX_DIFF; i++) {
        cnt += cnts[i];
        if (cnt >= k) return i;
    }
};

var smallestDistancePair = function(nums, k) {
    let n = nums.length;
    nums.sort((a, b) => a - b);
    let lo = 0, hi = nums[n - 1] - nums[0];

    let cnts = new Array(nums[n - 1] + 1).fill(0);
    let cntLessThan = new Array(nums[n - 1] + 1).fill(0);
    for (let num of nums) cnts[num]++;
    for (let i = 1; i <= nums[n - 1]; i++) cntLessThan[i] = cnts[i - 1] + cntLessThan[i - 1];

    const countPairDistSmallerThan = dist => {
        let cnt = 0;
        for (let i = 1; i < n; i++) {
            if (nums[i] <= dist) cnt += i;
            else cnt += i - cntLessThan[nums[i] - dist];
        }
        return cnt;
    };

    while (lo < hi) {
        let mid = ~~((lo + hi) / 2);
        if (countPairDistSmallerThan(mid) >= k) hi = mid;
        else lo = mid + 1; //smaller distance only has fewer pairs whose dist <= it.  
    }
    return lo;
};

smallestDistancePair = function(nums, k) {
    nums.sort((a, b) => a - b);
    let n = nums.length;
    let lo = 0, hi = nums[n - 1] - nums[0];

    const cntPairsSmallerThan = dist => {
        let cnt = 0, l = 0;
        for (let r = 0; r < n; r++) {
            while (nums[r] - nums[l] > dist) l++;
            cnt += r - l;
        }
        return cnt;
    };

    while (lo < hi) {
        let mid = ~~((lo + hi) / 2);
        let cnt = cntPairsSmallerThan(mid);
        if (cnt >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
};
```

---

## [K-th Smallest Prime Fraction](https://leetcode.com/problems/k-th-smallest-prime-fraction/description/)

> 本题与众不同
> candidate solution不一定存在于实际的数组里面
> 我们需要实时记录不大于candidate factor的最大的factor
> 每次确定新的搜索范围之后要重置最大factor为0.

```javascript
var kthSmallestPrimeFraction = function(A, K) {
    let n = A.length;
    let minHeap = new Heap(([i, j], [x, y]) => A[i] * A[n - 1 - y] - A[n - 1 - j] * A[x]);
    for (let i = 0; i < n; i++) minHeap.push([i, 0]);
    while (--K > 0) {
        let [i, j] = minHeap.pop();
        if (j < n - 1) minHeap.push([i, j + 1]);
    }
    let [i, j] = minHeap.pop();
    return [A[i], A[n - 1 - j]];
};

kthSmallestPrimeFraction = function(A, K) {
    let lo = 0, hi = 1;
    let p = 0, q = 1;
    let n = A.length;

    function cntLessEq(target) {
        let cnt = 0, j = n - 1;
        let p = 0, q = 1;//每次都要将 p/q reset = 0
        for (let i = 0; i < n; i++) {
            while (j >= 0 && A[i] > target * A[n - 1 - j]) j--;
            cnt += j + 1;
            if (j >= 0 && p * A[n - 1 - j] < q * A[i]) {
                p = A[i];
                q = A[n - 1 - j];
            }
        }
        return [cnt, p, q];
    }

    while (lo < hi) {
        let mid = (lo + hi) / 2;
        let [cnt, p, q] = cntLessEq(mid);
        if (cnt < K) lo = mid;
        else if (cnt > K) hi = mid;
        else {
            return [p, q];
        }
    }
};
```
---
