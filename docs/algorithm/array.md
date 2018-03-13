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
