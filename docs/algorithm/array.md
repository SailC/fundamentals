## [Find Pivot Index](https://leetcode.com/problems/find-pivot-index/description/)

`一遍过` `prefixsum`

0. bruteforce O(n^2)
> for each index, use O(n) to compute on the fly the leftSum & rightSum and see if they're equal

1. prefix sum (preprocessing) + array O(n)
> We need to quickly compute the sum of values to the left and the right of every index.
> Let's say we knew S as the sum of the numbers, and we are at index i. If we knew the sum of numbers leftsum that are to the left of index i, then the other sum to the right of the index would just be S - nums[i] - leftsum
> trade space for time

2. prefix on the fly
> use only a variable to represent prefixSum and commpute the suffixSum on the fly in O(1).
> O(1) space

```javascript
var pivotIndex = function(nums) {
    let n = nums.length;
    let left = new Array(n).fill(0), right = new Array(n).fill(0);
    let sumLeft = 0, sumRight = 0;
    for (let i = 0; i < n; i++) {
        [left[i], sumLeft] = [sumLeft, sumLeft + nums[i]];
        [right[n - 1 - i], sumRight] = [sumRight, sumRight + nums[n - 1 - i]];
    }
    for (let i = 0; i < n; i++) {
        if (left[i] === right[i]) return i;
    }
    return -1;
};

pivotIndex = function(nums) {
    let n = nums.length;
    let sum = nums.reduce((x, accSum) => x + accSum, 0);
    let prefixSum = 0;
    for (let i = 0; i < n; i++) {
        if (prefixSum === sum - nums[i] - prefixSum) return i;
        prefixSum += nums[i];
    }
    return -1;
};
```
---
## [Majority Element](https://leetcode.com/problems/majority-element/description/)

`hashmap` `sorting` `voting` `quick-select` `divide&conquery`

1. brute force O(n^2)
> iterates over the array, and then iterates again for each number to count its occurrences. As soon as a number is found to have appeared more than any other can possibly have appeared, return it.
2. hashmap O(n)
> We can use a HashMap that maps elements to counts in order to count occurrences in linear time by looping over nums. Then, we simply return the key with maximum value.
3. sorting O(nlgn)
If the elements are sorted in monotonically increasing (or decreasing) order, the majority element can be found at index `n/2` or `n/2 + 1` if even
4. divide & conqure O(nlogn)
> base case; the only element in an array of size 1 is the majority
> recurse on left and right halves of this slice.
> if the two halves agree on the majority element, return it.
> otherwise, count each element and return the "winner". O(n)
5. bit vote O(32 * n)
> 对每一位计算该bit的majority，也就是最后答案的bit
6. Boyer-Moore vote O(n)
> 每个数都check一下目前的candidate是不是自己，是的话投一票，不是的话减一，如果majority存在的话，投票的最后结果一定是majority.
7. quick select O(n)
> 求第 `n / 2` th number in the sorted array.

```javascript
var majorityElement = function(nums) {
    nums.sort((a, b) => a - b);
    let n = nums.length;
    return nums[~~(n / 2)];
};

majorityElement = function(nums) {
    let n = nums.length;
    let cntMap = new Map();
    for (let num of nums) cntMap.set(num, (cntMap.get(num) || 0) + 1);
    for (let num of cntMap.keys()) {
        if (cntMap.get(num) > ~~(n / 2)) return num;
    }
};

majorityElement = function(nums) {
    let vote = 0, candidate = 0;
    for (let num of nums) {
        if (vote === 0) candidate = num;
        if (num === candidate) vote++;
        else vote--;
    }
    return candidate;
};

majorityElement = function(nums) {
    let n = nums.length;
    let majority = 0;
    for (let i = 0; i < 32; i++) {
        let mask = 1 << i;
        let count = 0;
        for (let num of nums) {
            if (num & mask) count++;
        }
        if (count > ~~(n / 2)) majority |= mask;
    }
    return majority;
};
```

---
## [partition label](https://leetcode.com/problems/partition-labels/description/)

`一遍过` `回味` `partition` `greedy` `hashtable`

1. bruteforce
> Let's try to repeatedly choose the smallest left-justified partition
> For each letter encountered, process the last occurrence of that letter, extending the current partition [anchor, i] appropriately.
> invariant: `[anchor, i]` justified partition : each letter only appears in this partition
> for each char, use `O(n)` to find the last index of it.
2. hashtable
> use hashtable to preprocess the lastIndex info

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/763-ep161.png)

```javascript
var partitionLabels = function(S) {
    let indexMap = new Map();
    let n = S.length;
    for (let i = 0; i < n; i++) indexMap.set(S[i], i);
    let ans = [], max = 0, lastIdx = -1;
    for (let i = 0; i < n; i++) {
        let c = S[i];
        max = Math.max(max, indexMap.get(c));
        if (max === i) {
            ans.push(i - lastIdx);
            lastIdx = i;
        }
    }
    return ans;
};
```
---

## [Max chunks to make sorted](https://leetcode.com/problems/max-chunks-to-make-sorted/description/)
`无思路` `partition` `greedy`

1. left max & min right
> Iterate through the array, each time all elements to the left are smaller (or equal) to all elements to the right, there is a new chunk.

2. max so far
> keep track of the max value so far, if the current index equals the max value so far, increase the # of chunk by one.

```javascript
var maxChunksToSorted = function(arr) {
    let ans = 0, max = 0, n = arr.length;
    for (let i = 0; i < n; i++) {
        max = Math.max(max, arr[i]);
        if (max === i) ans++;
    }
    return ans;
};

maxChunksToSorted = function(arr) {
    let n = arr.length;
    let left = new Array(n), right = new Array(n);
    for (let i = 0; i < n; i++) {
        left[i] = i === 0 ? arr[i] : Math.max(left[i - 1], arr[i]);
    }
    for (let i = n - 1; i >= 0; i--) {
        right[i] = i === n - 1 ? arr[i] : Math.min(right[i + 1], arr[i]);
    }
    let ans = 1;
    for (let i = 0; i < n - 1; i++) {
        if (left[i] < right[i + 1]) ans++;
    }
    return ans;
};
```

---

## [Max chunks to make sorted II](https://leetcode.com/problems/max-chunks-to-make-sorted-ii/description/)

1. Mapping + reduce  O(nlgn)
> 将这题转换为 ver1.
> arr = [2, 3, 5, 4, 4]
> sorted = [2, 3, 4, 4, 5]
> indices = [0, 1, 4, 2, 3]
2. map + list + maxSofar O(nlgn)
> 在ver1 的基础上将indexMap拓展，value是index的list。这样每次extend window的时候就知道当前window的末尾index。
3. leftMax + rightMin O(n)
4. zip + cntMap O(nlgn)
> 原始数组和排序之后的数组在当前window出现的字符的个数相当才能切割.

`有思路` `不熟练` `greedy` `partition` `hashmap` `sort` `prefixsum`

```javascript
var maxChunksToSorted = function(arr) {
    let n = arr.length;
    let indexMap = new Map();
    let sorted = [...arr].sort((a, b) => a - b);
    for (let i = 0; i < n; i++) {
        if (!indexMap.has(sorted[i])) indexMap.set(sorted[i], []);
        indexMap.get(sorted[i]).push(i);
    }
    let max = 0, cnt = 0;
    for (let i = 0; i < n; i++) {
        let idx = indexMap.get(arr[i]).shift();
        max = Math.max(max, idx);
        if (i === max) cnt++;
    }
    return cnt;
};

maxChunksToSorted = function(arr) {
     let n = arr.length;
     let leftMax = new Array(n), rightMin = new Array(n);
     for (let i = 0; i < n; i++) {
         leftMax[i] = i === 0 ? arr[i] : Math.max(leftMax[i - 1], arr[i]);
     }
     for (let i = n - 1; i >= 0; i--) {
         rightMin[i] = i === n - 1 ? arr[i] : Math.min(rightMin[i + 1], arr[i]);
     }
     let cnt = 1;
     for (let i = 0; i < n - 1; i++) {
         if (leftMax[i] <= rightMin[i + 1]) cnt++;
     }
     return cnt;
 };

maxChunksToSorted = function(arr) {
    let n = arr.length;
    let sorted = [...arr].sort((a, b) => a - b);
    const zip = (a, b) => a.map((x, i) => [x, b[i]]);
    let cntMap = new Map();

    let cnt = 0;
    let diff = 0;
    for (let [x, y] of zip(arr, sorted)) {
        cntMap.set(x, (cntMap.get(x) || 0) + 1);
        if (cntMap.get(x) === 0) diff--;
        if (cntMap.get(x) === 1) diff++;

        cntMap.set(y, (cntMap.get(y) || 0) - 1);
        if (cntMap.get(y) === 0) diff--;
        if (cntMap.get(y) === -1) diff++;

        if (diff === 0) cnt++;
    }
    return cnt;
};
```
---
## [maximum swap](https://leetcode.com/problems/maximum-swap/description/)

1.  brute force
> The number only has at most 8 digits, so there are only C(8, 2) available swaps. We can easily brute force them all.
> Time: O(N ^ 2)
> Space: O(N) (convert temporary answer to array)

2. greedy
> 从左到右扫描digit，看看比该digit大的值存在不存在右边的数组。
> 从高到低值扫描，如果存在右边，则交换

3. dp
> 从左到右遍历数组
> 每次都看看有没有机会和右边值最大的那个交换
> 如果右边有多个最大值，和最右边的那个交换，这样可以使交换之后的数最大
> 所以要dp构建一个 dp[i] = nums[i: n)中最大值的最右idx

```javascript

var maximumSwap = function(num) {
    let lastIdx = new Array(10);
    num = String(num).split('').map(Number);
    let n = num.length;
    for (let i = 0; i < n; i++) lastIdx[num[i]] = i;

    for (let i = 0; i < n; i++) {
        for (let digit = 9; digit > num[i]; digit--) {
            if (lastIdx[digit] > i) {
                let idx = lastIdx[digit];
                [num[i], num[idx]] = [num[idx], num[i]];
                return Number(num.join(''));
            }
        }
    }

    return Number(num.join(''));
};

var maximumSwap = function(num) {
    num = String(num).split('').map(Number);
    let n = num.length;
    let maxVal = new Array(n).fill(-1);
    maxVal[n - 1] = n - 1;
    for (let i = n - 2; i >= 0; i--) {
        maxVal[i] = maxVal[i + 1];
        if (num[i] > num[maxVal[i + 1]]) maxVal[i] = i;
    }
    for (let i = 0; i < n - 1; i++) {
        let idx = maxVal[i + 1];
        if (num[idx] > num[i]) {
            [num[i], num[idx]] = [num[idx], num[i]];
            break;
        }
    }
    return Number(num.join(''));
};
```
---
## [maximum size subarray sum equal k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/description/)

> Speaking of consecutive subarray, we can use the difference : `Sum[0: j) - Sum[0: i) === Sum[i: j)`.
> it's easy to calculate running sums, but after that, shall we enumerate all the subarrays using the difference of the running sums ? if we do that, there're a total of n running sums, and `n ^ 2` subarrays.
> We don't want to enumerate all the subarrays, we just check the subarrays that matter to construct sum K.

1. two pass
> 1pass (constructe running sums) 2pass( for each `num[i]` we check if `target - num[i]` is available, and if so, we need to make sure that the subarray we checked is contained in the current subarray)
> To save the position info of the subarray, we use hashmap to map the `running sum` to `ending index`.
> Time: O(N)
> Space: O(2N)

2. one pass
> Since we're only interested in the subarray contained in the current subarray, we only look forward, which means we can use 1 pass to ensure that the subarray in the hashmap are only from the previous numbers.
> only update the ending index if it's not already in the map because we want to get the longest subarray

3. sliding window(if all input are positive)
> window rule, sum <= k

```javascript
var maxSubArrayLen = function(nums, k) {
    let n = nums.length;
    let sum = new Array(n + 1).fill(0);
    let idxMap = new Map([[0, 0]]);
    for (let i = 1; i <= n; i++) {
        sum[i] = nums[i - 1] + sum[i - 1];
        if (!idxMap.has(sum[i])) idxMap.set(sum[i], i);
    }
    //check subarray with sum
    let maxLen = 0;
    for (let i = 1; i <= n; i++) {
        let target = sum[i] - k;
        if (idxMap.has(target) && idxMap.get(target) < i) {
            maxLen = Math.max(maxLen, i - idxMap.get(target));
        }
    }
    return maxLen;
};

var maxSubArrayLen = function(nums, k) {
    let map = new Map([[0, 0]]);
    let n = nums.length, accSum = 0;
    let maxLen = 0;
    for (let i = 1; i <= n; i++) {
        accSum += nums[i - 1];
        let target = accSum - k;
        if (map.has(target)) {
            maxLen = Math.max(maxLen, i - map.get(target));
        }
        if (!map.has(accSum)) map.set(accSum, i);
    }
    return maxLen;
};
```
---
## [continuous subarray sum](https://leetcode.com/problems/continuous-subarray-sum/description/)

Key Observation:
> contiguous subarray `[i: j)` with sum = n * k => `sum[:i) % k === sum[:j) % k`

> if we see `accSum[i] % k === accSum[j] % k, i > j` then the segment `nums[i: j)` must be a mutiple of k
> `edge case`
> `k < 0` -> same as `k > 0`
> `k === 0`  -> `acc % k === NaN` , which indicates segement sum is zero -> `accSum[i] === accSum[j]`
> check if the segment size >= 2 before return

```javascript
var checkSubarraySum = function(nums, k) {
    k = Math.abs(k);
    let map = new Map();
    map.set(0, 0);
    let acc = 0;
    for (let i = 1; i <= nums.length; i++) {
        acc += nums[i - 1];
        let key = k === 0 ? acc: acc % k;
        if (map.has(key) && i - map.get(key) >= 2) {
            return true;
        }
        if (!map.has(key)) {
            map.set(key, i);
        }
    }
    return false;
};
```

## [contiguous array](https://leetcode.com/problems/contiguous-array/description/)

Key Observation:
> contiguous subarray `[i: j)` with equal num of 0 and 1s => `sum[:i) === sum[:j)` (if 0 is viewed as -1)

1. Bruteforce
> enumerate all contiguous array and count zeros and ones
> Time O(n ^ 2)
> Space O(1)

2. Hashtable looking backward
> Key Observation:
> If we see zero as -1, and one as + 1. And use that to calculate the running sum, if we saw `sum[i] === sum[j]` , then `nums[i + 1 : j]` must have same number of zeros and ones because they cancel each other.
> So we use hashtable to map `running sum` to ending index. Don't update the ending index if the running sum already in the map because we want to see the longest contiguous subarray.

```javascript
var findMaxLength = function(nums) {
    let maxLen = 0, n = nums.length;
    let map = new Map([[0, 0]]);//val -> idx
    let accSum = 0;
    for (let i = 1; i <= n; i++) {
        accSum += nums[i - 1] === 0 ? -1 : 1;
        if (map.has(accSum)) {
            maxLen = Math.max(maxLen, i - map.get(accSum));
        } else {
            map.set(accSum, i);
        }
    }
    return maxLen;
};
```
---
## [product of array except self](https://leetcode.com/problems/product-of-array-except-self/description/)

1. Running Product
> Use accumulative product , update it along the way from left to right and save the partial product to the result array. Then do it the second time from right to left.
> init the accumulative product to be 1 for the corner case `i == 0 || i == n - 1`.
> update the result product using the acc product first.
> then update he acc product with the current number.

```javascript
var productExceptSelf = function(nums) {
    let n = nums.length;
    let products = new Array(n).fill(1);

    // fill the left running products
    let accProduct = 1;
    for (let i = 0; i < n; i++) {
        products[i] *= accProduct;
        accProduct *= nums[i];
    }

    // fill the right running products
    accProduct = 1;
    for (let i = n - 1; i >= 0; i--) {
        products[i] *= accProduct;
        accProduct *= nums[i];
    }
    return products;
};
```
---
## [move zeros](https://leetcode.com/problems/move-zeroes/description/)

> All elements before the slow pointer (lastNonZeroFoundAt) are non-zeroes.
> All elements between the current and slow pointer are zeroes.
> this invariant continous all the way to the end, where we have the rest of our array filled with 0s.

```javascript
var moveZeroes = function(nums) {
    const isNonZero = x => x !== 0;
    let i = 0; // cnt of nonZero elements
    for (let j = 0; j < nums.length; j++) {
        if (isNonZero(nums[j])) {
            [nums[i], nums[j]] = [nums[j], nums[i]];
            i++;
        }
    }
};
```

---

## [merge sorted array](https://leetcode.com/problems/merge-sorted-array/description/)

`invariant + two pointers`
> invariant is `nums1[k + 1:]` has been filled with the largest elements of the merged sorted array.
> To maintain that invariant, we need to compare the end of the two array and pick the bigger one to push to the invariant.
> The only concern is whether we will pollute the first array by writing to the end of the first array. The answer is no.

Let's consider the extreme cases here :
`nums1 = [1,2,3, _, _], nums2 = [4, 5]` in this case, `nums1` will be left untouched

`nums1 = [4, 5, _, _, _], nums2 = [1,2]` in this case, `nums1` will be move to the end, and the original value is no needed any more.

So the point is , the original values will be either untouched or moved to the end before it's being overwritten by nums2

```javascript
// nums1 = [2, 4, 6, _, _, _]
// nums2 = [4, 7, 8]  
var merge = function(nums1, m, nums2, n) {
    let i = m - 1, j = n - 1, k = m + n - 1;
    while (i >= 0 && j >= 0) {
        if (nums1[i] > nums2[j]) {
            nums1[k--] = nums1[i--];
        } else {
            nums1[k--] = nums2[j--];
        }
    }
    while (j >= 0) nums1[k--] = nums2[j--];
};
```
---
## [remove duplicates from sorted array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/description/)

1. `invariant + two pointers`
> we maintain an invariant `nums[0: cnt)` only contains uniq number.
> we compare the `nums[i]` to the last element in the invariant, (which is at most `nums[i - 1]` ),
we ony add to the invariant if they're not the same

```javascript
var removeDuplicates = function(nums) {
    let cnt = 0; // len of the new array
    for (let num of nums) {
        if (cnt < 1 || nums[cnt - 1] !== num) nums[cnt++] = num;
    }
    return cnt;
};
```
---
## [remove duplicate from sorted array](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/description/)

> we maintain an invariant `nums[0: cnt)` only contains two dup number in a row.
> we compare the `nums[i]` to the second to last element in the invariant, (which is at most `nums[i - 2]`),
> we ony add to the invariant if they're not the same.

```javascript
var removeDuplicates = function(nums) {
    let cnt = 0; //pointer of the new uniq array
    for (let num of nums) {
        if (cnt < 2 || num !== nums[cnt - 2]) nums[cnt++] = num;
    }
    return cnt;
};
```
---
## [sort colors](https://leetcode.com/problems/sort-colors/description/)

1. `count colors`
> First, iterate the array counting number of 0's, 1's, and 2's, then overwrite array with total number of 0's, then 1's and followed by 2's.
2. `invariant + two pointers`
> `nums[0:redIdx)` contains all red ,
> `nums[blueIdx + 1:]` contains all blue.
> The idea is to move all 0s to the left, & all 2s to the right. Then all 1s are left in the middle.
> if RED is met, swap it to the red section, the swapped element is either RED or WHITE, because blue would be swapped to the blue section already.
> tricky part is when swapped element from blue section is possble to be red, so we can't really `i++` , and need to swap the red in the next round.

```javascript
var sortColors = function(nums) {
    let n = nums.length;
    const R = 0, G = 1, B = 2;
    let r = 0, b = n - 1;
    for (let i = 0; i <= b; ) {
        let color = nums[i];
        if (color === G) i++;
        else if (color === R) {
            [nums[i], nums[r]] = [nums[r], nums[i]];
            r++;
            i++;
        } else {
            [nums[i], nums[b]] = [nums[b], nums[i]];
            b--;
        }
    }
};
```
---
## [increasing triplet sequence](https://leetcode.com/problems/increasing-triplet-subsequence/description/)

> keep track of two smallest values,  as soon as we find a number bigger than both, while both have been updated, return true.
> 这个mid要比当前num小，同时他要大于某个之前的值，
> 所以要更新小的mid，才能让num容易大于它
> 同时为了得到尽可能小的mid，我们也需要更新小的small来是得满足条件的mid更多

```javascript
var increasingTriplet = function(nums) {
    let smallest = Infinity, mid = Infinity;
    for (let num of nums) {
        if (num <= smallest) {
            smallest = num;
        } else if (num <= mid) {
            mid = num;
        } else {// smallest < mid < num
            return true;
        }
    }
    return false;
};
```
---
## [sparse matrix multiplication](https://leetcode.com/problems/sparse-matrix-multiplication/description/)

1. brute force
> for each C[ i ] [ j ], it uses C[ i ] [ j ] += A[ i ] [ k ] * B[ k ] [ j ] where k = [ 0, n].Note: even A[ i ] [ k ] or B[ k ] [ j ] is 0, the multiplication is still executed.
2. prune
if A[ i ] [ k ] == 0 or B[ k ] [ j ] == 0, it just skip the multiplication . This is achieved by moving for-loop" for ( k = 0; k < n; k++ ) " from inner-most loop to middle loop, so that we can use if-statement to tell whether A[ i ] [ k ] == 0 or B[ k ] [ j ] == 0. This is really smart.

```javascript
var multiply = function(A, B) {
    let l = A.length;
    if (l === 0) return [[]];
    let m = A[0].length;
    let n = B[0].length;
    let C = new Array(l).fill(0).map(x => new Array(n).fill(0));
    for (let i = 0; i < l; i++) {
        for (let j = 0; j < n; j++) {
            for (let k = 0; k < m; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    return C;
};

multiply = function(A, B) {
    let m = A.length, n = A[0].length, nB = B[0].length;
    let C = new Array(m).fill(0).map(x => new Array(nB).fill(0));

    for (let i = 0; i < m; i++) {
        for (let k = 0; k < n; k++) {
            if (A[i][k] !== 0) {
                for (let j = 0; j < nB; j++) {
                    if (B[k][j] !== 0) C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
    return C;
};
```
---

## [intersection of two arrays](https://leetcode.com/problems/intersection-of-two-arrays/description/)

```
1. two hash set => intersection
2. sort two array + dedup + two pointers
3. sort two array + binary search
```

```javascript
// Two pointers O(nlgN)
var intersection = function(nums1, nums2) {
    nums1.sort((a, b) => a - b);
    nums2.sort((a, b) => a - b);
    let i = 0, j = 0;
    let inter = [];
    while (i < nums1.length && j < nums2.length) {
        if (i > 0 && nums1[i - 1] === nums1[i]) {
            i++;
            continue;
        }
        if (j > 0 && nums2[j - 1] === nums2[j]) {
            j++;
            continue;
        }
        if (nums1[i] === nums2[j]) {
            inter.push(nums1[i]);
            i++;
            j++;
        }
        else if (nums1[i] < nums2[j]) i++;
        else j++;
    }
    return inter;
};

// Binary Search O(nlgn)
var intersection = function(nums1, nums2) {
    nums1.sort((a, b) => a - b);
    nums2.sort((a, b) => a - b);
    let inter = [];
    function binarySearch(nums, target) {
        let lo = 0, hi = nums.length - 1;
        while (lo < hi) {
            let mid = lo + ~~((hi - lo) / 2);
            if (target === nums[mid]) return mid;
            if (target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        }
        return target === nums[lo] ? lo : -1;
    }
    for (let i = 0; i < nums1.length; i++) {
        if (i > 0 && nums1[i] === nums1[i - 1]) continue;
        let j = binarySearch(nums2, nums1[i]);
        if (j !== -1) inter.push(nums1[i]);
    }
    return inter;
};

// hashset O(n)
var intersection = function(nums1, nums2) {
    let set1 = new Set(nums1);
    let set2 = new Set(nums2);
    return [...set1].filter(x => set2.has(x));
}
```

---

## [intersection of two arrays II ](https://leetcode.com/problems/intersection-of-two-arrays-ii/description/)

```javascript
var intersect = function(nums1, nums2) {
    let cntMap = new Map();
    for (let num of nums1) cntMap.set(num, (cntMap.get(num) || 0) + 1);

    let result = [];
    for (let num of nums2) {
        if ( (cntMap.get(num) || 0) > 0 ) {
            result.push(num);
            cntMap.set(num, (cntMap.get(num) || 0) - 1);
        }
    }

    return result;
};

intersect = function(nums1, nums2) {
    // sort two arrs
    nums1.sort((a, b) => a - b);
    nums2.sort((a, b) => a - b);
    // set two pointers
    let i = 0, j = 0;
    let result = [];
    while (i < nums1.length && j < nums2.length) {
        if (nums1[i] === nums2[j]) {
            result.push(nums1[i]);
            i++;
            j++;
        } else if (nums1[i] < nums2[j]) {
            i++;
        } else {
            j++;
        }
    }
    return result;
};
```

---

## [intersection of two linked list](https://leetcode.com/problems/intersection-of-two-linked-lists/description/)

```javascript
var getIntersectionNode = function(headA, headB) {
    let lenA = 0, lenB = 0;
    for (let node = headA; node; node = node.next) lenA++;
    for (let node = headB; node; node = node.next) lenB++;
    if (lenA > lenB) {
        [headA, headB] = [headB, headA]; // make sure headA's path is shorter
        [lenA, lenB] = [lenB, lenA];
    }
    for (let i = 0; headB && i < lenB - lenA; headB = headB.next) i++; // headA should be in the same depth has headB
    while (headA && headB) {
        if (headA === headB) return headA;
        headA = headA.next;
        headB = headB.next;
    }
    return null;

};
```

I 可用hashset来记录两个set，然后求intersection
也可用sort + two pointers / binary search 来求解

II 运行result有duplicate， hashset就要变成hashmap用来记录剩余可用的相同元素
同样可以使用two pointer，而且不用判重更简单
Q. What if the given array is already sorted? How would you optimize your algorithm? If both arrays are sorted, I would use two pointers to iterate, which somehow resembles the merge process in merge sort.

Q. What if nums1's size is small compared to nums2's size? Which algorithm is better?
Suppose lengths of two arrays are N and M, the time complexity of my solution is O(N+M) and the space complexity if O(N) considering the hash. So it's better to use the smaller array to construct the counter hash.
Q. What if elements of nums2 are stored on disk, and the memory is limited such that you cannot load all elements into the memory at once?
Divide and conquer. Repeat the process frequently: Slice nums2 to fit into memory, process (calculate intersections), and write partial results to memory.

对于linked list 这题，先计算高度差，然后将比较高的那个右移直到高度差一样。
然后同时前进知道相遇或者有一个null

两个排序的数组， 写出intersection and union 两个function.
Union 直接开一个set，往里面加数

---

## [shortest unsorted continuous subarray](https://leetcode.com/problems/shortest-unsorted-continuous-subarray/description/)

> keep tracker of the occurence of `nums[i] < nums[j]`
find the left boundary, min[i]
and the right boundary, max[j]

> The idea behind this method is that the correct position of the minimum element in the unsorted subarray helps to determine the required left boundary. Similarly, the correct position of the maximum element in the unsorted subarray helps to determine the required right boundary.

```javascript
var findUnsortedSubarray = function(nums) {
    let sorted = [...nums].sort((a, b) => a - b);
    let lo = 0, hi = nums.length - 1;
    while (lo < hi) {
        if (nums[lo] === sorted[lo]) lo++;
        else if (nums[hi] === sorted[hi]) hi--;
        else break;
    }
    let len = hi - lo + 1;
    return len === 1 ? 0: len;
};

findUnsortedSubarray = function(nums) {
    let lo = 0, hi = nums.length - 1, max = -Infinity, min = Infinity;
    //find two boundary
    while (lo < hi && nums[lo] <= nums[lo + 1]) lo++;
    if (lo >= hi) return 0;
    while (nums[hi] >= nums[hi - 1]) hi--;
    // calc the min &max
    for (let i = lo; i <= hi; i++) {
        max = Math.max(max, nums[i]);
        min = Math.min(min, nums[i]);
    }
    // extend the unsorted arr
    while (lo > 0 && nums[lo - 1] > min) lo--;
    while (hi < nums.length - 1&& nums[hi + 1] < max) hi++;
    return hi - lo + 1;

}
```
---

## [summary ranges](https://leetcode.com/problems/summary-ranges/description/)

The array is sorted and without duplicates. In such array, two adjacent elements have difference either 1 or larger than 1. If the difference is 1, they should be put in the same range; otherwise, separate ranges.

We also need to know the start index of a range so that we can put it in the result list. Thus, we keep two indices, representing the two boundaries of current range. For each new element, we check if it extends the current range. If not, we put the current range into the list.

Don't forget to put the last range into the list. One can do this by either a special condition in the loop or putting the last range in to the list after the loop.

```javascript
var summaryRanges = function(nums) {
    let n = nums.length;
    if (n === 0) return [];
    let i = 0, ranges = [];
    for (let j = 1; j <= n; j++) {
        if (j === n || nums[j] !== nums[j - 1] + 1) {
            let len = j - i;
            if (len === 1) {
                ranges.push(`${nums[i]}`);
            } else {
                ranges.push(`${nums[i]}->${nums[j - 1]}`);
            }
            i = j;
        }
    }
    return ranges;
};
```

---

## [shortest word distance](https://leetcode.com/problems/shortest-word-distance/description/)

> 1. linear scan + update pointers

``` javascript
var shortestDistance = function(words, word1, word2) {
    let dist = Number.MAX_VALUE;
    let p1 = -1, p2 = -1; // haven't found target word yet
    for (let i = 0; i < words.length; i++) {
        let word = words[i];
        // update pointers if found target
        if (word === word1) p1 = i;
        if (word === word2) p2 = i;
        // update dist if possible
        if (p1 !== -1 && p2 !== -1) dist = Math.min(dist, Math.abs(p1 - p2));
    }
    return dist;
};
```

---

## [shortest word distance ii](https://leetcode.com/problems/shortest-word-distance-ii/description/)

> 1. index map + two pointers

```javascript
var WordDistance = function(words) {
    this.indexMap = new Map();
    for (let i = 0; i < words.length; i++) {
        let word = words[i];
        if (!this.indexMap.has(word)) this.indexMap.set(word, []);
        this.indexMap.get(word).push(i);
    }
};

WordDistance.prototype.shortest = function(word1, word2) {
    let [indices1, indices2] = [word1, word2].map(x => this.indexMap.get(x));
    let minDist = -1;
    let i = 0, j = 0;
    while (i < indices1.length && j < indices2.length) {
        let idx1 = indices1[i], idx2 = indices2[j];
        if (idx1 < idx2) {
            if (minDist === -1 || idx2 - idx1 < minDist) minDist = idx2 - idx1;
            i++;
        } else {
            if (minDist === -1 || idx1 - idx2 < minDist) minDist = idx1 - idx2;
            j++;
        }
    }
    return minDist;
};
```

---

## [shortest word distance iii](https://leetcode.com/problems/shortest-word-distance-iii/description/)

1. linear scan, update two points
> 分类讨论 word1 === word2 && word1 !== word2 的情况

```javascript
var shortestWordDistance = function(words, word1, word2) {
    let shortest = Infinity;
    if (word1 === word2) {
        let prev = -1;
        for (let i = 0; i < words.length; i++) {
            let word = words[i];
            if (word === word1) {
                if (prev !== -1) shortest = Math.min(shortest, i - prev);
                prev = i;
            }
        }
    } else {
        let p1 = -1, p2 = -1;
        for (let i = 0; i < words.length; i++) {
            let word = words[i];
            if (word === word1) p1 = i;
            if (word === word2) p2 = i;
            if (p1 !== -1 && p2 !== -1) shortest = Math.min(shortest, Math.abs(p1 - p2));
        }
    }
    return shortest;
};
```

---

## [subarray sum equals k](https://leetcode.com/problems/subarray-sum-equals-k/description/)

1. accSum + hashMap

```javascript
var subarraySum = function(nums, k) {
    let n = nums.length;
    let accSum = 0;
    let sumMap = new Map();
    let cnt = 0;
    sumMap.set(0, 1);
    for (let i = 0; i < nums.length; i++) {
        accSum += nums[i];
        let target = accSum - k;
        cnt += sumMap.get(target) || 0;
        sumMap.set(accSum, (sumMap.get(accSum) || 0) + 1);
    }
    return cnt;
};
```

---

## [subarray product less than k](https://leetcode.com/problems/subarray-product-less-than-k/description/)

1. prodSum + search for letmost prodSum > prod / k
2. sliding window

```javascript
var numSubarrayProductLessThanK = function(nums, k) {
    let cnt = 0;
    let n = nums.length;
    let accProd = new Array(n).fill(1);
    for (let i = 0; i < n; i++) accProd[i] = i === 0 ? nums[i] : (nums[i] * accProd[i - 1]);
    for (let i = 0; i < n; i++) {
        if (accProd[i] < k) cnt += i + 1;
        else {
            let idx = binSearch(accProd, 0, i - 1, accProd[i] / k);
            if (idx < i) cnt += i - idx;
        }
    }
    return cnt;
};

function binSearch(arr, lo, hi, target) {
    while (lo < hi) {
        let mid = lo + ~~((hi - lo) / 2);
        if (arr[mid] <= target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return arr[lo] > target ? lo : lo + 1;
}

var numSubarrayProductLessThanK = function(nums, k) {
    if (k <= 1) return 0;
    let prod = 1, total = 0, i = 0;
    for (let j = 0; j < nums.length; j++) {
        prod *= nums[j];
        while (prod >= k) {
            prod /= nums[i];
            i++;
        }
        total += j - i + 1;
    }
    return total;
};
```

---

## [two sum](https://leetcode.com/problems/two-sum/description/)
`一遍过` `回味`

1. bruteforce
> for each nums[i], check if there's a num[j] (j > i) that nums[i] + nums[j] === target.
> if so, return [i, j]
> Time: O(n^2)
> space: O(1)

2. hashtable
> Use hashtable to save the `number to index` mapping
> Time: O(n)
> Space: O(n)

```javascript
var twoSum = function(nums, target) {
    let map = new Map();
    for (let i = 0; i < nums.length; i++) {
        let num = nums[i];
        if (map.has(target - num)) return [map.get(target - num), i];
        map.set(num, i);
    }
    return -1;
};
```
---

## [two sum II](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)

```javascript
var twoSum = function(numbers, target) {
    let lo = 0, hi = numbers.length - 1;

    while (lo < hi) {
        let sum = numbers[lo] + numbers[hi];
        if (sum === target) return [lo + 1, hi + 1];
        if (sum < target) lo++;
        else hi--;
    }

    return [-1, -1];

};
```


---
## [three sum](https://leetcode.com/problems/3sum/description/)

> 外层循环是以 nums[i] 为第一个元素的3 sum，将第一个解作为uniq解进行skip dup
> 如果是作为解的第一个元素，那么是依赖相同序列的第一个元素，if (i > 0 && nums[i] === nums[i - 1]) skip
> 如果是作为解的最后一个元素，依赖相同序列的最后一个元素， if (i < n - 1 && nums[i] === nums[i + 1]) skip

1. Sort + TwoPointers
> 内层循环以 nums[lo] 作为第一个元素的 2sum，将第一个解作为uniq解进行skip dup
> Time: O(n ^ 2)
> Space: O(1)

2.  Sort + HashTable
> 内层循环以 nums[i] 作为最后一个元素的 2sum，将最后一个解作为uniq解
> Time : O(n ^ 2)
> Space: O(n)


```javascript
var threeSum = function(nums) {
    // sorted array makes it easy to skip duplicates & use two pointers
    nums.sort((a, b) => a - b);
    let triplets = [];
    for (let i = 0; i < nums.length; i++) {
        if (i > 0 && nums[i] === nums[i - 1]) continue;
        let doublets = twoSum(nums, i + 1, nums.length - 1, -nums[i]);
        for (let doublet of doublets) triplets.push([nums[i], ...doublet]);
    }
    return triplets;
};

function twoSum (nums, lo, hi, target) {
    let visited = new Set();
    let result = [];
    for (let i = lo; i <= hi; i++) {
        if (i < hi && nums[i] === nums[i + 1]) {
            visited.add(nums[i]);
            continue;
        }
        if (visited.has(target - nums[i])) {
            result.push([target - nums[i], nums[i]]);
        }
        visited.add(nums[i]);
    }
    return result;
}

function twoSum (nums, lo, hi, target) {
    let result = new Set();
    let [left, right] = [lo, hi];
    while (lo < hi) {
        if (lo > left && nums[lo] === nums[lo - 1]) {
            lo++;
            continue;
        }
        if (nums[lo] + nums[hi] === target) {
            result.add([nums[lo++], nums[hi--]]);
        } else if (nums[lo] + nums[hi] < target) {
            lo++;
        } else {
            hi--;
        }
    }
    return result;
}
```
