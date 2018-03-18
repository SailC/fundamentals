# Dynamic Programming

## [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/description/)

1. divide & conquer
> `O(n)`uan
2. dp
> `dp[i] = Math.max(dp[i - 1] + nums[i - 1], nums[i - 1]);`

```
#!/bin/bash
var maxSubArray = function(nums) {
    let n = nums.length;
    //let dp = new Array(n + 1).fill(0);
    let curMax = 0;
    let maxVal = -Infinity;
    for (let i = 1; i <= n; i++) {
        //dp[i] = Math.max(dp[i - 1] + nums[i - 1], nums[i - 1]);
        curMax = Math.max(curMax + nums[i - 1], nums[i - 1]);
        // maxVal = Math.max(maxVal, dp[i]);
        maxVal = Math.max(maxVal, curMax);
    }
    return maxVal;
};

maxSubArray = function(nums) {
    let n = nums.length;

    function maxSub(lo, hi) {
        if (lo > hi) return -Infinity;
        let mid = lo + ~~((hi - lo) / 2);
        let maxSum = nums[mid];
        let sum = nums[mid];
        for (let i = mid - 1; i >= 0; i--) {
            sum += nums[i];
            maxSum = Math.max(maxSum, sum);
        }
        sum = maxSum;
        for (let i = mid + 1; i < n; i++) {
            sum += nums[i];
            maxSum = Math.max(maxSum, sum);
        }
        return Math.max(maxSum, maxSub(lo, mid - 1), maxSub(mid + 1, hi));
    }

    return maxSub(0, n - 1);
};
```

---
## [Partition equal subset sum](https://leetcode.com/problems/partition-equal-subset-sum/description/)

`有思路` `dp` `recursion`

> find if the array can be partitioned into two subsets such that the sum of elements in both subsets is equal. in other words, find if there's a sub set whose sum is `sum / 2`.
> So this is not a continuous subseq (sub array problem) but a (subset, subseq) problem.

1. recursion + memorization
> `canHalf(start, acc)` means with acc , `nums[start:]` can find half of the sum.
2. dp.
>  `recursive subproblem`
> `dp[i][j]` means we can find target sum === j within `nums[0: i)` .
> for each `nums[i]`, we can do two things:
> 1) we can either count on the previous subarrays to find target sum
> 2) we can use `nums[i]` and count on the previous subarrays to find `target sum - nums[i]`
> `dp[i][j] === dp[i - 1][j] || dp[i - 1][j - nums[i - 1]]` (note that `j - nums[i - 1]` >=  0)
> `edge case`
> `dp[i][0] = true` since we can also find empty set to make a sum of zero.
> `dp[0][j] = false` for all i > 0

```javascript
var canPartition = function(nums) {
    let sum = nums.reduce((x, acc) => x + acc, 0);
    if (sum % 2 > 0) return false;
    let target = sum / 2;
    let n = nums.length;
    let cache = new Array(n + 1).fill(0).map(x => new Array(target + 1).fill(null));

    function canHalf(start, acc) {
        if (start === n || acc * 2 >= sum) {
            return acc * 2 === sum;
        }
        if (cache[start][acc] !== null) return cache[start][acc];
        cache[start][acc] = canHalf(start + 1, acc + nums[start]) || canHalf(start + 1, acc);
        return cache[start][acc];
    }

    return canHalf(0, 0);
};

canPartition = function(nums) {
    let sum = nums.reduce((x, acc) => x + acc, 0);
    if (sum % 2 > 0) return false;
    let target = sum / 2;
    let n = nums.length;
    let dp = new Array(n + 1).fill(0).map(x => new Array(target + 1).fill(false));
    for (let i = 0; i <= n; i++) dp[i][0] = true;
    //dp[0][i] === false, i > 0
    for (let i = 1; i <= n; i++) {
        let num = nums[i - 1];
        for (let j = 1; j <= target; j++) {//bug j - num >= 0
            dp[i][j] = dp[i - 1][j] || (j - num >= 0 && dp[i - 1][j - num]);
        }
    }
    return dp[n][target];
};
```
---
## [Partition to K equal Sum subset](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/description/)
`有思路` `回味` `backtracking` `dp` `combination`

1. greedy
> try to push as many element to k groups as possible, if all elements can be pushed to `group[i]` without violating `group[i] <= target` , then in the end all groups sum to `target`
> say we have four groups `g0, g1, g2, g3` , target is 4, sum = 16, if in the end `g0 < 4` then there must be a group whose sum `> 4` to reach the sum 16.
> Time: O(k ^ N)

2. dfs
>  The dfs process is to find a subset of nums[] which sum equals to sum/k. We use an array visited[] to record which element in nums[] is used. Each time when we get a cur_sum = sum/k, we will start from position `0->n` in nums[] to look up the elements that are not used yet and find another cur_sum = sum/k.
>  Time: O(N ^ k)

3. dp
> dp[# of set combination] . Our goal is to use nums in some order so that placing them into groups in that order will be valid. search(used, ...) will answer the question: can we partition unused elements of nums[i] appropriately?
> `(todo - 1) % target + 1` 是一个绝妙的判定，想想看你还有和为todo这么多的数要去安置，而你要把他们分别安置到和大小为target的partition，这个时候我们先要填充那个填充了一半的partition了，可填充的值得大小在`(todo - 1) % target + 1` ，最大填充target，相当于一次性填充空块， 最小填充1。
> edge case `dp[1 << n - 1] = true` 当所有的num都被合理安置完毕
> Time : T(N * 2 ^ N)

```javascript
var canPartitionKSubsets = function(nums, k) {
    let sum = nums.reduce((acc, x) => acc + x, 0);
    let [target, remainder] = [sum / k, sum % k];
    if (remainder !== 0) return false;
    nums.sort((a, b) => b - a);
    if (nums[0] > target) return false;
    let n = nums.length;
    let visited = new Array(n).fill(false);

    function canPart(start, accSum, groupNum) {
        if (groupNum === 0) return true;
        if (accSum > target) return false;
        if (accSum === target) return canPart(0, 0, groupNum - 1);
        for (let i = start; i < n; i++) {
            if (visited[i]) continue;
            visited[i] = true;
            if (canPart(i + 1, accSum + nums[i], groupNum)) return true;
            visited[i] = false;
        }
        return false;
    }

    let groups = new Array(k).fill(0);
    function greedyPart(start) {
        if (start === n) return true;
        let num = nums[start];
        for (let i = 0; i < k; i++) {
            if (groups[i] + num > target) continue;
            groups[i] += num;
            if (greedyPart(start + 1)) return true;
            groups[i] -= num;
        }
        return false;
    }

    //return canPart(0, 0, k);
    return greedyPart(0);
};

canPartitionKSubsets = function(nums, k) {
    let sum = nums.reduce((acc, x) => acc + x, 0);
    let [target, remainder] = [sum / k, sum % k];
    if (remainder !== 0) return false;
    nums.sort((a, b) => b - a);
    if (nums[0] > target) return false;
    let n = nums.length;
    let cache = new Array(1 << n).fill(null);
    cache[(1 << n) - 1] = true;

    function search(used, todo) {
        if (cache[used] === null) {
            let limit = ((todo - 1) % target) + 1;
            cache[used] = false;
            for (let i = 0; i < n; i++) {
                if (((used >>> i) & 1) === 0 && nums[i] <= limit) {
                    if (search(used | (1 << i), todo - nums[i])) {
                        cache[used] = true;
                        break;
                    }
                }
            }
        }
        return cache[used];
    }

    return search(0, sum);
};
```
---
## [Can I win](https://leetcode.com/problems/can-i-win/description/)
`有思路` `回味` `combination`

1. recursion + mem
> a total of `O(2 ^ N)` state, for each state, use a local variable `accSum` to keep track of the sum of that state, the currently player can win in the current state if the other playbook can lose in any of the the next state.
> edge case `when desiredTotal === 0` in the beginning, the player win. when inside the recursion, the play lose because the other one reaches the total first.
> edge case II, when the given num's sum is smaller than total, return false.
> Time complexity O(2 ^ N * N)

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/02/464-ep165-2.png)

```javascript
var canIWin = function(maxChoosableInteger, desiredTotal) {
    let n = maxChoosableInteger;
    let nums = [...new Array(n).keys()].map(x => x + 1);
    let sum = nums.reduce((acc, x) => acc + x, 0);
    if (sum < desiredTotal) return false;
    let cache = new Array((1 << n)).fill(null);
    const visited = (state, i) => ((state >>> i) & 1) === 1;
    const setVisit = (state, i) => state | (1 << i);

    function canWin(state, accSum) {
        if (cache[state] !== null) return cache[state];
        if (accSum >= desiredTotal) return false;
        cache[state] = false;
        for (let i = 0; i < n; i++) {
            if (visited(state, i)) continue;
            if (!canWin(setVisit(state, i), accSum + nums[i])) {
                cache[state] = true;
                break;
            }
        }
        return cache[state];
    }

    return desiredTotal === 0 || canWin(0, 0); //bug
};
```
---
## [Flip Game II](https://leetcode.com/problems/flip-game-ii/description/)

`一遍过` `backtrack + mem`

1. backtracking + mem
> edge case, when no '++' in the string exist for the player to flip
> playA wins if any of the playerB's next move loses
> Time: O(2 ^ N) , for each '++', either playerA will take this move or B
> withtout memorization, time complexity would be O(N!) because each current move can generate O(N - 1) next moves in the worst case `+++++++`.

```javascript
var canWin = function(s) {
    let n = s.length;
    let cache = new Map();
    function can(s) {
        if (cache.has(s)) return cache.get(s);
        cache.set(s, false);
        for (let i = 2; i <= n; i++) {
            if (s.slice(i - 2, i) === '++') {
                if (!can(s.slice(0, i - 2) + '--' + s.slice(i))) {
                    cache.set(s, true);
                }
            }
        }
        return cache.get(s);
    }
    return can(s);
};
```
---
## [Predict the winner](https://leetcode.com/problems/predict-the-winner/description/)

`有思路` `不熟练` `backtracking + mem` `dp` `minmax`

1. backtracking without mem
> player's goal is to maximize the score, while cpu is to minimize the score
> see if the final score of the player is >= 0
> time: O(2 ^ n)  Size of recursion tree will be 2^n. Here, n refers to the length of nums array.
> space: O(n) the depth of recursion tree

2. backtracking with mem
> time: O(n ^ 2) The entire cache of size n x n is filled only once.
> space: O(n ^ 2) cache.

3. 2D dp
> `dp[i, j] = Max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j -1])`
> time: O(n^2)
> space: O(n ^ 2)

4. 1D dp
> only the entries in the next row(same column) and the previous column(same row) are needed.
> Instead of making use of a new row in dpdp array for the current dpdp row's updations, we can overwrite the values in the previous row itself and consider the values as belonging to the new row's entries, since the older values won't be needed ever in the future again
> `dp[i + 1][j]` 就是自己当前的值，`dp[i][j - 1]`就是 current row的前面求好的值（当前行的update而不是前面行的update）
> 如果recursive function依赖于前面行的update，那么需要保证前面行的update不被overwrite

![thoughts](https://leetcode.com/problems/predict-the-winner/Figures/486/486_Predict_the_winner_new.PNG)

```javascript
var PredictTheWinner = function(nums) {
    let n = nums.length;
    let cache = new Array(n).fill(0).map(x => new Array(n).fill(null));
    function winner(lo, hi, player) {
        if (lo === hi) return player ? nums[lo] : -nums[lo];
        if (cache[lo][hi] !== null) return cache[lo][hi];
        let a = (player ? nums[lo] : -nums[lo]) + winner(lo + 1, hi, !player);
        let b = (player ? nums[hi] : -nums[hi]) + winner(lo, hi - 1, !player);
        cache[lo][hi] = player ? Math.max(a, b) : Math.min(a, b);
        return cache[lo][hi];
    }
    return winner(0, nums.length - 1, true) >= 0;
};

PredictTheWinner = function(nums) {
    let n = nums.length;
    let dp = new Array(n).fill(0).map(x => new Array(n).fill(0));
    for (let i = 0; i < n; i++) dp[i][i] = nums[i];
    for (let i = n - 2; i >= 0; i--) {
        for (let j = i + 1; j < n; j++) {
            let a = nums[i] - dp[i + 1][j];
            let b = nums[j] - dp[i][j - 1];
            dp[i][j] = Math.max(a, b);
        }
    }
    return dp[0][n - 1] >= 0;
};

PredictTheWinner = function(nums) {
    let n = nums.length;
    let dp = new Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) {
        for (let j = i; j < n; j++) {
            if (i === j) {
                dp[i] = nums[i];
                continue;
            }
            let a = nums[i] - dp[j];
            let b = nums[j] - dp[j - 1];
            dp[j] = Math.max(a, b);
        }
    }
    return dp[n - 1] >= 0;
};
```

---
## [guess number higher or lower](https://leetcode.com/problems/guess-number-higher-or-lower-ii/description/)

`有思路` `aha` `dp` `minmax`

1. recursion without mem
> 人类的目的是最小化 cost.
> CPU的目的是最大化 cost
> 所以人类的对策是，考虑CPU所有最大化cost的结果，然后将其最小化.
> we can pick up any number ii in the range (1, n). Assuming it is a wrong guess(worst case scenario), we have to minimize the cost of reaching the required number.
> Time: O(n!). We have to pick n numbers in the worst case, each time we need to find a minCost pivot in O(n) time
> space: O(n) recursion of depth n

2. dp
> Same idea. Time: O(n ^ 3). We fill in the dp matrix once, for each entry we take O(n) to compute .
> space: O(n ^ 2)

```javascript
var getMoneyAmount = function(n) {
    let cache = new Array(n + 1).fill(0).map(x => new Array(n + 1).fill(-1));
    function moneyToWin(lo, hi) {
        if (lo >= hi) return 0;
        if (cache[lo][hi] !== -1) return cache[lo][hi];
        let paid = Infinity;
        for (let pick = lo; pick <= hi; pick++) {
            let a = pick + moneyToWin(pick + 1, hi);
            let b = pick + moneyToWin(lo, pick - 1);
            paid = Math.min(paid, Math.max(a, b));
        }
        cache[lo][hi] = paid;
        return paid;
    }
    return moneyToWin(1, n);
};

getMoneyAmount = function(n) {
    let dp = new Array(n + 2).fill(0).map(x => new Array(n + 2).fill(0));
    for (let i = n; i >= 1; i--) {
        for (let j = i + 1; j <= n; j++) {
            dp[i][j] = Infinity;
            for (let k = i; k <= j; k++) {
                dp[i][j] = Math.min(dp[i][j], k + Math.max(dp[k + 1][j], dp[i][k - 1]))
            }
        }
    }
    return dp[1][n];
};
```
---
## [target sum](https://leetcode.com/problems/target-sum/description/)
`经典` `dp` `01backpack`

![thoughts1](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-2.png)
![thoughts2](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-1.png)
![thoughts3](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-3.png)
![thoughts4](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-4.png)
![thoughts5](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-5.png)
![thoughts6](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-6.png)
![thoughts7](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/494-ep156-7.png)

1. brute force (dfs)
> time : O(2 ^ n)
> space: O(n)

2. dp (2D -> 1D)
> why dp works better? 因为dfs是在枚举符号的组合，而dp则是在枚举sum，search space小了很多.
> dp[i][j] means # of ways that `nums[0:i)` can be sumed to `j`
> goal: `dp[n][S + sum]` sum is the offset in case the S < 0
> always check `j - num` && `j + num` to prevent out of bound error
> edge case : `dp[0][offset + 0] = 1`,
> since `dp[i][j] = dp[i - 1][j - num] + dp[i - 1][j + num]`, it depends on i - 1, we can use rolling array to make it 1D dp.
> time : O(n * sum)
> space: O(n * sum) -> O(sum)

3. 0-1 backpack
> since each num can either be in  + or - group, our goal is to find subset of nums that are in + group such that `sum(+group) === (sum(all) + target) / 2` . this converts the problem to find a subsequence of array with a particular sum.
> `dp[i][j]` means the # of subsequence in `nums[0:i)` that sum to j.
> `dp[i][j]` = `dp[i - 1][j]` + `dp[i - 1][j - num]`
> goal: `dp[n][target]`  
> time: O(n * target)
> space: O(n * target) -> O(target)

```javascript
var findTargetSumWays = function(nums, S) {
    let n = nums.length;
    let sum = nums.reduce((acc, x) => acc + x, 0);
    if (sum < Math.abs(S)) return 0;

    let cache = new Array(n + 1).fill(0).map(x => new Array(2 * sum + 1).fill(-1));

    function ways(start, acc, target) {
        if (start === n) {
            return acc === target ? 1 : 0;
        }
        let key = acc + sum;
        if (cache[start][key] !== -1) return cache[start][key];
        let num = nums[start];
        cache[start][key] = ways(start + 1, acc + num, target) + ways(start + 1, acc - num, target);
        return cache[start][key];
    }

    return ways(0, 0, S);
};

findTargetSumWays = function(nums, S) {
    let n = nums.length;
    let sum = nums.reduce((acc, x) => acc + x, 0);
    if (sum < Math.abs(S)) return 0;

    let dp = new Array(n + 1).fill(0).map(x => new Array(2 * sum + 1).fill(0));
    dp[0][sum] = 1;

    for (let i = 1; i <= n; i++) {
        let num = nums[i - 1];
        for (let j = 0; j < 2 * sum + 1; j++) {
            let a = (j - num >= 0) ? dp[i - 1][j - num] : 0;
            let b = (j + num < 2 * sum + 1) ? dp[i - 1][j + num] : 0;
            dp[i][j] = a + b;
        }
    }

    return dp[n][S + sum];
};

findTargetSumWays = function(nums, S) {
    let n = nums.length;
    let sum = nums.reduce((acc, x) => acc + x, 0);
    if (sum < Math.abs(S)) return 0;

    let dp = new Array(2 * sum + 1).fill(0);
    dp[sum] = 1;

    for (let i = 1; i <= n; i++) {
        let num = nums[i - 1];
        let tmp = new Array(2 * sum + 1).fill(0);
        for (let j = 0; j < 2 * sum + 1; j++) {
            let a = (j - num >= 0) ? dp[j - num] : 0;
            let b = (j + num < 2 * sum + 1) ? dp[j + num] : 0;
            tmp[j] = a + b;
        }
        dp = tmp;
    }

    return dp[S + sum];
};

findTargetSumWays = function(nums, S) {
    let n = nums.length;
    let sum = nums.reduce((acc, x) => acc + x, 0);
    let [target, remain] = [(sum + S) / 2, (sum + S) % 2];
    if (sum < Math.abs(S) || remain !== 0) return 0;

    let dp = new Array(target + 1).fill(0);
    dp[0] = 1;

    for (let num of nums) {
        for (let j = sum; j >= num; j--) {
            dp[j] += dp[j - num];
        }
    }

    return dp[target];
};
```
---
## [Coin Change](https://leetcode.com/problems/coin-change/description/)
`经典` `dp` `backtracking+mem` `可用无限次`

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/322-ep148.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/322-ep148-2.png)

1. recursion without mem
> each coin can be used unilmited number of times, try all combinations of the coins and prune the search if overflow
> each nodes as a start coin and a accSum with it, gather the count of all children that can lead to valid combination and find the minimum of it
> time: O(amount ^ N) branching factor is n, in the worst case, the recursion tree can have depth of amount. [1,1,1,1...]

2. dp
> `dp[i][j]` means the minumn number of coins picking from `nums[0:i)` that sum to `j`.
> `dp[i][j] = min(dp[i -1][j], 1 + dp[i][j - coin_i])`
> 一个是使用一枚或者多枚coin_i, 一个是不适用coin_i(直接使用之前的coin type，成功连接到子问题)
> time: O(amount * N)
> space: O(amount * N) -> O(amount)

```javascript
var coinChange = function(coins, amount) {
    let n = coins.length;
    coins.sort((a, b) => b - a);
    let cache = new Array(n + 1).fill(0).map(x => new Array(amount + 1).fill(null));

    function numCoins(start, accSum) {
        if (accSum >= amount) {
            return accSum === amount ? 0 : Infinity;
        }
        if (cache[start][accSum] !== null) return cache[start][accSum];
        let count = Infinity;
        for (let i = start; i < n; i++) {
            let cnt = numCoins(i, accSum + coins[i]);
            if (cnt !== Infinity) count = Math.min(count, 1 + cnt);
        }
        cache[start][accSum] = count;
        return count;
    }
    let count = numCoins(0, 0);
    return count === Infinity ? -1 : count;
};

coinChange = function(coins, amount) {
    let n = coins.length;
    let dp = new Array(n + 1).fill(0).map(x => new Array(amount + 1).fill(Infinity));
    for (let i = 0; i <= n; i++) dp[i][0] = 0;
    for (let i = 1; i <= n; i++) {
        let coin = coins[i - 1];
        for (let j = 0; j <= amount; j++) {
            let a = dp[i - 1][j];
            let b = (j - coin >= 0) ? (1 + dp[i][j - coin]) : Infinity;
            dp[i][j] = Math.min(a, b);
        }
    }
    return dp[n][amount] === Infinity ? -1: dp[n][amount];
};

coinChange = function(coins, amount) {
    let n = coins.length;
    let dp = new Array(amount + 1).fill(Infinity);
    dp[0] = 0;
    for (let coin of coins) {
        for (let j = 0; j <= amount; j++) {
            let a = dp[j];
            let b = (j - coin >= 0) ? (1 + dp[j - coin]) : Infinity;
            dp[j] = Math.min(a, b);
        }
    }
    return dp[amount] === Infinity ? -1: dp[amount];
};
```
---
## [combination sum IV](https://leetcode.com/problems/combination-sum-iv/description/)

`一遍过` `回味` `recursion+mem` `dp`

`diff from combSumI, II, III`
> 1. it's asking for a number of possible combs, not all combs. So a lot of overlapps
> 2. different sequence (order) can be counted as different combs, so we need to scan every num in each level of dfs.

`key observation` :
> (1,1, 2)  & (1,2,1)  are counted as different combinations
> so we don't need to sort the num to avoid duplicates.

`recursive sub structure`
> try to add the next number to the combination , if possible, add the possible number of combination of the rest of the numbers.

`overlap`  
> for `[1,2,3, ...]`, `comb1 = [1,2, ...]`, comb2 = [3, ...]  the sub problem is the same. you can always start from the first num to last num and add it to the combination if it's not leading to a overflow.
> only target number matters, the position of the newly added number does not matter.

时间复杂度
> Time : O(target * |nums|)
> Space: O(target)
这里用recursion + mem 的平均时间复杂度其实要优于bottom up的dp，因为后者要计算所有target的值，而前者可以跳过无意义的target值，只计算必须计算的target的，所以前者的复杂度其实是 O(sum{target / num_i})

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/377-ep135.png)

```javascript
var combinationSum4 = function(nums, target) {
    let cache = new Array(target + 1).fill(-1);
    function dfs(acc) {
        if (acc >= target) {
            return acc === target ? 1 : 0;
        }
        if (cache[acc] !== -1) return cache[acc];
        cache[acc] = 0;
        for (let num of nums) {
            cache[acc] += dfs(acc + num);
        }
        return cache[acc];
    }
    return dfs(0);
};

combinationSum4 = function(nums, target) {
    let dp = new Array(target + 1).fill(0);
    dp[0] = 1;
    for (let i = 1; i <= target; i++) {
        for (let num of nums) {
            if (i - num >= 0) {
                dp[i] += dp[i - num];
            }
        }
    }
    return dp[target];
};
```
---
## [House Robber](https://leetcode.com/problems/house-robber/description/)
`一遍过` `回味` `dp`
> 状态转移和buy & sell stock 异曲同工

1. bruteforce
for each house , decide whether to rob it or not. `2^n` combination of choices.
2. recursion + mem
3. dp with robNorob space O(1)
> rob[i] max money after robbing house i , noRob[i] max money after not robbing house i
4. dp with maxRob(ornot) space O(n)
> dp[i] mx money after robbing / not robbing house i
5. dp with maxRob(ornot) space O(1)

```javascript
var rob = function(nums) {
    let n = nums.length;
    let cache = new Array(n).fill(-1);
    function robFrom(i) {
        if (i >= n) return 0;
        if (cache[i] !== -1) return cache[i];
        cache[i] = Math.max(nums[i] + robFrom(i + 2), robFrom(i + 1));
        return cache[i];
    }
    return robFrom(0);
};

rob = function(nums) {
    let rob = 0, noRob = 0;
    for (let num of nums) {
        [rob, noRob] = [noRob + num, Math.max(rob, noRob)];
    }
    return Math.max(rob, noRob);
};

rob = function(nums) {
    let n = nums.length;
    // max money after visiting house[i]
    let dp = new Array(n + 1).fill(0);
    dp[1] = nums[0];
    for (let i = 2; i <= n; i++) {
        dp[i] = Math.max(nums[i - 1] + dp[i - 2], dp[i - 1]);
    }
    return dp[n];
};

rob = function(nums) {
    let n = nums.length;
    // max money after visiting house[i]
    let f2 = 0, f1 = 0;
    for (let i = 0; i < n; i++) {
        [f1, f2] = [Math.max(nums[i] + f2, f1), f1];
    }
    return f1;
};
```
---
## [House Robber II](https://leetcode.com/problems/house-robber-ii/description/)
`套路` `dp`

1. dp
> 可以利用house rob I.
> 只不过需要分类讨论，
> case1: house[0] gets robbed, house[1] & house[n - 1] can't be robbed , 其余随意
> case2: house[0] not robbed, 其余随意

```javascript
var rob = function(nums) {
    let n = nums.length;
    if (n === 0) return 0;
    return Math.max(nums[0] + robI(nums, 2, n - 2), robI(nums, 1, n - 1));
};

var robI = function(nums, lo, hi) {
    let rob = 0, noRob = 0;
    for (let i = lo; i <= hi; i++) {
        let curRob = nums[i] + noRob;
        let curNoRob = Math.max(rob, noRob);
        rob = curRob;
        noRob = curNoRob;
    }
    return Math.max(rob, noRob);
};
```
---
## [Delete and earn](https://leetcode.com/problems/delete-and-earn/description/)

`无思路` `回味` `dp`

1. brute force + hashtable
> use a hashtable to cnt the appearance of each number
> during each call, try to pick a number to delete and move its adj numbers
> Time: O(N ^ N) in the worst case, no numbers are adj, so recurse N levels, each level have N choice
> We can optimize a bit by delete the whole entry at a level, which make T = O(N!) , each level has N - 1 choice
2. dp
> reduce to house robber problem
> Time: O(N + R) , R is the max val of the nums
> Space: O(R)

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/740-ep125.png)

```javascript
var deleteAndEarn = function(nums) {

    let cache = new Map();

    function earn(cntMap) {
        if (cntMap.size === 0) return 0;
        //let key = JSON.stringify(cntMap);//bug
        let key = [...cntMap].toString();
        if (cache.has(key)) return cache.get(key);

        let maxProfit = 0;
        for (let [num, cnt] of cntMap) {
            let map = new Map(cntMap);
            for (let adj of [num - 1, num + 1]) map.delete(adj);
            map.set(num, cnt - 1);
            if (map.get(num) === 0) map.delete(num);
            maxProfit = Math.max(maxProfit, num + earn(map));
        }
        cache.set(key, maxProfit);
        return cache.get(key);
    }

    let cntMap = new Map();
    for (let num of nums) cntMap.set(num, (cntMap.get(num) || 0) + 1);
    return earn(cntMap);
};

deleteAndEarn = function(nums) {
    if (nums.length === 0) return 0;
    let maxVal = Math.max(...nums); //bug when nums = []
    let earn = new Array(maxVal + 1).fill(0);
    for (let num of nums) earn[num] += num;
    return rob(earn);
};

rob = function(nums) {
    let n = nums.length;
    // max money after visiting house[i]
    let f2 = 0, f1 = 0;
    for (let i = 0; i < n; i++) {
        [f1, f2] = [Math.max(nums[i] + f2, f1), f1];
    }
    return f1;
};
```

---

## [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/description/)
`一遍过` `dfs + mem -> dp`

1. dfs
> `cost(i,j)=grid[i][j]+min(cost(i+1,j),cost(i,j+1))`
> edge case : when `i >= m || j >= n || (i === m - 1 && j === n - 1)`
> Time complexity : `O(2 ^ (m + n))` For every move, we have at most 2 options and we have `m + n` moves from topleft to bottomright.
2. dfs + mem
> There could be mutiple calls to the same (i, j). So we use a 2d cache to cache the result.
> Time complexity : `O(m*n)` each cache cell is generated once in `O(1)` time.
3. dp (2d -> 1d)
> same idea, just with extra edge cases reprensent with array element and save the space from `O(m*n) to `O(n)`
4. dp with no extra space
> instead of using a extra matrix we can just use grid itself.

```javascript
var minPathSum = function(grid) {
    let m = grid.length, n = grid[0].length;
    let cache = new Array(m).fill(0).map(x => new Array(n).fill(-1));

    function dfs(i, j) {
        if (i === m || j === n) return Infinity;
        if (i === m - 1 && j === n - 1) return grid[i][j];
        if (cache[i][j] !== -1) return cache[i][j];
        cache[i][j] = grid[i][j] + Math.min(dfs(i + 1, j), dfs(i, j + 1));
        return cache[i][j];
    }

    return dfs(0, 0);
};

minPathSum = function(grid) {
    let m = grid.length, n = grid[0].length;
    // let dp = new Array(m).fill(0).map(x => new Array(n).fill(Infinity));
    let dp = new Array(n).fill(Infinity);

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            // if (i === 0 && j === 0) dp[i][j] = grid[i][j];
            if (i === 0 && j === 0) dp[j] = grid[i][j];
            else if (i === 0) dp[j] = grid[i][j] + dp[j - 1];
            else if (j === 0) dp[j] = grid[i][j] + dp[j];
            // else dp[i][j] = grid[i][j] + Math.min(dp[i - 1][j], dp[i][j - 1]);
            else dp[j] = grid[i][j] + Math.min(dp[j], dp[j - 1]);
        }
    }
    //return dp[0][0]
    return dp[n - 1];
};

minPathSum = function(grid) {
    let m = grid.length, n = grid[0].length;
    // let dp = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(Infinity));

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (i === 0 && j === 0) continue;
            if (i === 0) grid[i][j] += grid[i][j - 1];
            else if (j === 0) grid[i][j] += grid[i - 1][j];
            else grid[i][j] = grid[i][j] + Math.min(grid[i - 1][j], grid[i][j - 1]);
        }
    }

    return grid[m - 1][n - 1];
};
```
---
## [decode ways](https://leetcode.com/problems/decode-ways/description/)

`有思路` `backtracking+mem` `dp`

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/91-ep103-1.png)
![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/91-ep103-2.png)

> 和wordbreak 基本一样
> 只不过 return value 从 boolean变成number
> matching candidate 变少了，只能match first digit or first two digits.

```javascript
var numDecodings = function(s) {
    let n = s.length;
    if (n === 0) return 0;
    let codeMap = new Set();
    for (let code = 1; code <= 26; code++) {
        codeMap.add(String(code));
    }
    let cache = new Array(n + 1).fill(-1);

    function decode(i) {
        if (i === n) return 1;
        if (cache[i] !== -1) return cache[i];
        let takeOneDigit = codeMap.has(s[i]) ? decode(i + 1) : 0;
        let takeTwoDigit = (i < n - 1 && codeMap.has(s.slice(i, i + 2))) ? decode(i + 2) : 0;
        cache[i] = takeOneDigit + takeTwoDigit;
        return cache[i];
    }

    return decode(0);
};

var numDecodings = function(s) {
    if (s.length === 0) return 0;

    let codeSet = new Set();
    for (let i = 1; i <= 26; i++) codeSet.add(String(i));
    let dp = new Array(s.length + 1);
    dp[0] = 1;
    for (let i = 1; i <= s.length; i++) {
        let takeOneDigit = codeSet.has(s.slice(i - 1, i)) ? dp[i - 1] : 0;
        let takeTwoDigit = (i >= 2 && codeSet.has(s.slice(i - 2, i))) ? dp[i - 2] : 0;
        dp[i] = takeOneDigit + takeTwoDigit;
    }
    return dp[s.length];
};

var numDecodings = function(s) {
    if (s.length === 0) return 0;
    let codeSet = new Set();
    for (let i = 1; i <= 26; i++) codeSet.add(String(i));
    let f2 = 1, f1 = codeSet.has(s[0]) ? 1 : 0;
    for (let i = 2; i <= s.length; i++) {
        let takeOneDigit = codeSet.has(s.slice(i - 1, i)) ? f1 : 0;
        let takeTwoDigit = codeSet.has(s.slice(i - 2, i)) ? f2 : 0;
        [f2, f1] = [f1, takeOneDigit + takeTwoDigit];
    }
    return f1;
};
```
---
## [decode ways ii](https://leetcode.com/problems/decode-ways-ii/description/)

`有思路` `分类讨论` `计数dp`

> 使用 recursion + mem 栈溢出

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/639-ep110-1-1.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/639-ep110-2.png)

```javascript
var numDecodings = function(s) {
    let n = s.length;
    let cache = new Array(n).fill(-1);
    const kMod = 1000000007;
    function decode(start) {
        if (start >= n) return 1;
        if (cache[start] !== -1) return cache[start];
        let ways = 0;
        ways += takeOne(s[start]) * decode(start + 1);
        if (start < n - 1)
            ways += takeTwo(s[start], s[start + 1]) * decode(start + 2);
        cache[start] = (ways + kMod) % kMod;
        return cache[start];
    }

    return decode(0);
};

numDecodings = function(s) {
    let n = s.length;
    let dp = new Array(n + 1).fill(0);
    dp[0] = 1;
    const kMod = 1000000007;

    for (let i = 1; i <= n; i++) {
        dp[i] += takeOne(s[i - 1]) * dp[i - 1];
        if (i > 1) {
            dp[i] += takeTwo(s[i - 2], s[i - 1]) * dp[i - 2];
        }
        dp[i] = (dp[i] + kMod) % kMod;
    }

    return dp[n];
};

function takeOne(c) {
    if (c === '0') return 0;
    if (c === '*') return 9;
    return 1;
}

function takeTwo(c1, c2) {
    if (c1 === '*' && c2 === '*') return 15;
    if (c1 === '*') {
        return Number(c2) > 6 ? 1 : 2;
    } else if (c2 === '*') {
        if (c1 === '1') return 9;
        if (c1 === '2') return 6;
        return 0;
    } else {
        if (c1 === '1') return 1;
        if (c1 === '2') return Number(c2) <= 6 ? 1 : 0;
        return 0;
    }
}
```
---
## [domino tiling](https://leetcode.com/problems/domino-and-tromino-tiling/description/)

`无思路` `矩阵dp` `几何`

> 列数多tiling可以由列数更少的tiling拼上不同形状的骨牌达到
> 列出状态转移方程就可以求解

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/02/790-ep171.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/02/790-ep171-2.png)

```javascript
var numTilings = function(N) {
    const kMod = 1000000007;
    let dp = new Array(N + 1).fill(0).map(x => new Array(3).fill(0));
    dp[0][0] = dp[1][0] = 1;
    for (let i = 2; i <= N; i++) {
        dp[i][0] = (dp[i - 1][0] + dp[i - 2][0] + dp[i - 1][1] + dp[i - 1][2]) % kMod;
        dp[i][1] = (dp[i - 2][0] + dp[i - 1][2]) % kMod;
        dp[i][2] = (dp[i - 2][0] + dp[i - 1][1]) % kMod;
    }
    return dp[N][0];
};
```
---
## [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/)

`一遍过` `回味` `dp`

![Thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/121-ep140-1.png)

```javascript
var maxProfit = function(prices) {
    let lo = prices[0], n = prices.length;
    let maxPro = 0;
    for (let i = 1; i < n; i++) {
        let profit = prices[i] - lo;
        maxPro = Math.max(maxPro, profit);
        lo = Math.min(lo, prices[i]);
    }
    return maxPro;
};

maxProfit = function(prices) {
    let n = prices.length;
    let sold = 0, hold = -Infinity;
    for (let price of prices) {
        sold = Math.max(sold, price + hold);
        hold = Math.max(hold, -price);
    }
    return sold;
};

maxProfit = function(prices) {
    let n = prices.length;
    let gain = [];
    for (let i = 1; i < n; i++) gain.push(prices[i] - prices[i - 1]);
    return maxSubArr(gain);
}

function maxSubArr(gain) {
    let n = gain.length;
    let maxVal = 0, curVal = 0;
    for (let i = 0; i < n; i++) {
        curVal = Math.max(gain[i], gain[i] + curVal);
        maxVal = Math.max(maxVal, curVal);
    }
    return maxVal;
}
```
---

## [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/)

1. greedy
> try to trade every day if there's profit
> 一个大trade可以看成几个小trade
2. dp
> 其实state machine 和localmax是一回事，只不过state machine思路更清晰，localMax似乎是为了加速被迫为之。

```javascript
var maxProfit = function(prices) {
    let profit = 0;
    for (let i = 1; i < prices.length; i++) {
        let dayTrade = prices[i] - prices[i - 1];
        if (dayTrade > 0) profit += dayTrade;
    }
    return profit;
};

maxProfit = function(prices) {
    let n = prices.length;
    if (n === 0) return 0;
    let dp = new Array(n).fill(0);
    let localMax = dp[0] - prices[0];
    for (let i = 1; i < n; i++) {
        dp[i] = Math.max(dp[i - 1], prices[i] + localMax);
        localMax = Math.max(localMax, dp[i] - prices[i]);
    }
    return dp[n - 1];
}

maxProfit = function(prices) {
    let hold = -Infinity, sold = 0;
    for (let price of prices) {
        let prevHold = hold;
        hold = Math.max(hold, sold - price);
        sold = Math.max(sold, prevHold + price);
    }
    return sold;
};
```
---
## [best time to buy and sell stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/description/)

> at the end of each day i, we can do two things:
> 1) use the chance, complete a trade, update the max profit
> 2) wait for better timing by holding the chance and use the previous max profit.
> localMax和hold/sold模型最大的区别是，hold/sold明确指出day i时候的status是买完还是买完，而localMax模型则都可以，所以localMax模式dp[i]泛指profit，而不涉及状态.
1. one + two
> solve the problem with only one transaction limit, then solve the two transaction limit based on the previous solution

```javascript
var maxProfit = function(prices) {
    if (prices.length === 0) {
        return 0;
    }
    let one = new Array(prices.length).fill(0);
    let minPrice = prices[0];
    for (let i = 1; i < prices.length; i++) {
        one[i] = Math.max(0, prices[i] - minPrice, one[i - 1]);
        minPrice = Math.min(minPrice, prices[i]);
    }
    let two = new Array(prices.length).fill(0);
    //two[i] = max(two[i - 1], Max(one[j] + price[i] - price[j], j < i) )
    let localMax = one[0] - prices[0];
    for (let i = 1; i < prices.length; i++) {
        two[i] = Math.max(two[i - 1], prices[i] + localMax);
        localMax = Math.max(localMax, one[i] - prices[i]);
    }
    return Math.max(...two);
};

maxProfit = function(prices) {
    let n = prices.length;
    let hold1 = new Array(n + 1).fill(-Infinity);
    let sold1 = new Array(n + 1).fill(0);
    for (let i = 1; i <= n; i++) {
        hold1[i] = Math.max(hold1[i - 1], -prices[i - 1]);
        sold1[i] = Math.max(sold1[i - 1], prices[i - 1] + hold1[i - 1]);
    }
    let hold2 = new Array(n + 1).fill(-Infinity);
    let sold2 = new Array(n + 1).fill(0);
    for (let i = 1; i <= n; i++) {
        hold2[i] = Math.max(hold2[i - 1], hold1[i], sold1[i - 1] - prices[i - 1]);
        sold2[i] = Math.max(sold2[i - 1], sold1[i], hold2[i - 1] + prices[i - 1]);
    }
    return sold2[n];
};
```
---

## [best time to buy and sell stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/description/)

> if `k >= ~~(n / 2)` then we can do as many transaction as possible (for [1,2], we can do at most 1 transaction).

```javascript
var maxProfit = function(k, prices) {
    let n = prices.length;
    if (k >= ~~(n / 2)) return maxProfitII(prices);
    let dp = new Array(k + 1).fill(0).map(x => new Array(n + 1).fill(0));
    for (let i = 1; i <= k; i++) {
        let localMax = -Infinity;
        for (let j = 1; j <= n; j++) {
            dp[i][j] = Math.max(dp[i][j - 1], prices[j - 1] + localMax)
            localMax = Math.max(localMax, dp[i - 1][j] - prices[j - 1]);
        }
    }
    return dp[k][n];
};

maxProfit = function(k, prices) {
    let n = prices.length;
    if (k >= ~~(n / 2)) return maxProfitII(prices);
    let hold = new Array(k + 1).fill(0).map(x => new Array(n + 1).fill(-Infinity));
    let sold = new Array(k + 1).fill(0).map(x => new Array(n + 1).fill(0));
    for (let i = 1; i <= k; i++) {
        for (let j = 1; j <= n; j++) {
            hold[i][j] = Math.max(hold[i][j - 1], hold[i - 1][j], sold[i - 1][j - 1] - prices[j - 1]);
        }
        for (let j = 1; j <= n; j++) {
            sold[i][j] = Math.max(sold[i][j - 1], sold[i - 1][j], hold[i][j - 1] + prices[j - 1]);
        }
    }
    return sold[k][n];
};

var maxProfitII = function(prices) {
    let profit = 0;
    for (let i = 1; i < prices.length; i++) {
        let dayTrade = prices[i] - prices[i - 1];
        if (dayTrade > 0) profit += dayTrade;
    }
    return profit;
};
```
---
## [best time to buy and sell stock with cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description/)

> 将问题抽象为一个状态机，买卖只是动作，不同状态由动作产生，保存profit在状态变量里面，状态变量随着天数和动作改变。

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/309-ep150.png)

```javascript
var maxProfit = function(prices) {
    let sold = 0, rest = 0, hold = -Infinity;
    for (let price of prices) {
        let prevSold = sold;
        sold = hold + price;
        hold = Math.max(hold, rest - price);
        rest = Math.max(rest, prevSold);
    }
    return Math.max(rest, sold);
};
```
---

## [Min cost climbing stairs](https://leetcode.com/problems/min-cost-climbing-stairs/description/)

`一遍过` `回味` `dp`

1. recursion + mem
2. dp with space O(n) 爬到stair i, 还未离开（付钱）
3. dp with space O(n) 爬到stair i, 离开（付钱）之后
4. dp with space O(1) 爬到stair i, 还未离开（付钱）
5. dp with space O(1) 爬到stair i, 离开（付钱）之后

```javascript
var minCostClimbingStairs = function(cost) {
    let n = cost.length;
    let cache = new Array(n + 2).fill(-1);
    function climbCost(start) {//从stair i出发，付钱之后的cost
        if (start >= n) return 0;
        if (cache[start] !== -1) return cache[start];
        cache[start] = Math.min(climbCost(start + 1), climbCost(start + 2)) + cost[start];
        return cache[start];
    }
    return Math.min(climbCost(0),climbCost(1));
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, dp = new Array(n + 1).fill(0);
    for (let i = 2; i <= n; i++) {//爬到stair i, 还未离开（付钱）之前的cost
        dp[i] = Math.min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
    }
    return dp[n];
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, f1 = 0, f2 = 0;
    for (let i = 2; i <= n; i++) {//爬到stair i, 还未离开（付钱）之前的cost
        [f1, f2] = [Math.min(f1 + cost[i - 1], f2 + cost[i - 2]), f1];
    }
    return f1;
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, dp = new Array(n + 1).fill(0);
    dp[0] = cost[0];
    dp[1] = cost[1];
    for (let i = 2; i < n; i++) {//爬到stair i, 离开（付钱）之后的cost
        dp[i] = Math.min(dp[i - 1], dp[i - 2]) + cost[i];
    }
    return Math.min(dp[n - 1], dp[n - 2]);
};

minCostClimbingStairs = function(cost) {
    let n = cost.length, f2 = cost[0], f1 = cost[1];
    for (let i = 2; i < n; i++) {//爬到stair i, 离开（付钱）之后的cost
        [f1, f2] = [Math.min(f1, f2) + cost[i], f1];
    }
    return Math.min(f1, f2);
};
```
---
## [cherry pick](https://leetcode.com/problems/cherry-pickup/description/)

`巨难` `matrix dp`

> 不能用贪心连续min path sum两次，因为这两次的动作会互相影响
> 自由度(x1, y1, x2)只有三维，第四维由前三位决定，所以三维dp
> 每次行动有四种方式，DD, DR, RD, RR.

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/741-ep123.png)

```javascript
var cherryPickup = function(grid) {
    let n = grid.length;
    let cache = new Array(n).fill(0).map(x => new Array(n).fill(0).map(x => new Array(n).fill(-Infinity))); //3D array set to -Infinity to indicate no answer
    // -Infinity means unknow result, -1 means blocked, >= 0 means cherry picked along the way to destination
    function pick(x1, y1, x2) {
        const y2 = x1 + y1 - x2; //bind two actions
        if (x1 >= n || x2 >= n || y1 >= n || y2 >= n) return -1; // out of bound
        if (grid[y1][x1] < 0 || grid[y2][x2] < 0) return -1; // blocked
        if (x1 === n - 1 && y1 === n - 1) return grid[y1][x1]; // destination
        if (cache[x1][y1][x2] !== -Infinity) return cache[x1][y1][x2]; // cached
        let cherry = Math.max( //DD, DR, RR, RD
            pick(x1 + 1, y1, x2),
            pick(x1 + 1, y1, x2 + 1),
            pick(x1, y1 + 1, x2 + 1),
            pick(x1, y1 + 1, x2)
        );
        if (cherry < 0) cache[x1][y1][x2] = -1; //no way to go
        else {
            cherry += grid[y1][x1];//A picked his cherry
            if (x1 !== x2) cherry += grid[y2][x2]; //B picked his if he's not in the same position with A
            cache[x1][y1][x2] = cherry; // cache the result
        }
        return cache[x1][y1][x2];
    }

    return Math.max(0, pick(0, 0, 0));//start from the src
};
```
---
## [burst ballons](https://leetcode.com/problems/burst-balloons/description/)

`无思路` `bottom up` `逆向dp`

> topdown dfs 的思路是先爆气球，再去计算子问题，这样子每次爆完气球，子问题的气球融合了，这样子问题的数据就变成 O(2 ^ n) 每个气球都可以选择爆还是不爆
> bottom up 思路是先爆子问题，爆剩下的气球用来增加coin
> `dp[i][j]` 表示 `nums[i:j]` 气球爆炸所得到的coins.
> 由于爆炸的时候要顺便带走左右边界两个倒霉气球，而子问题爆炸之后他们的气球消失，所以左右边界的气球分别称为 `i -1` `j + 1`
> 为了计算方便，事先搞两个fake ballon放在左右两边.
> TIme: O(N ^ 3) , a total of N ^ 2 state, each takes O(N) to compute

![1][./images/4.png]

```javascript
var maxCoins = function(nums) {
    let n = nums.length;
    nums = [1, ...nums, 1];//fake ballons for edge case
    let cache = new Array(n + 2).fill(0).map(x => new Array(n + 2).fill(-1));

    function burst(i, j) {
        if (i > j) return 0;
        if (i === j) return nums[i - 1] * nums[i] * nums[j + 1];
        if (cache[i][j] !== -1) return cache[i][j];
        let maxCoins = 0;
        for (let k = i; k <= j; k++) {
            maxCoins = Math.max(maxCoins, nums[i - 1] * nums[k] * nums[j + 1] + burst(i, k - 1) + burst(k + 1, j));
        }
        cache[i][j] = maxCoins;
        return maxCoins;
    }

    return burst(1, n);
};
```
---
## [count different palindrom subsequences](https://leetcode.com/problems/count-different-palindromic-subsequences/description/)

`有思路` `分类讨论` `计数dp`

1. search
> Time: O(N * 2 ^N) 枚举所有subsequence and check isPalin
2. dp
> 当两边（哨兵）字母一样的时候，分三种情况讨论,
> 1) 中间的子串不包含哨兵的时候
> 2) 中间包含一个哨兵字母
> 3) 包含两个或以上哨兵字母
> Time: O(N ^ 2)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/730-ep114-1.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/730-ep114-2.png)

```javascript
var countPalindromicSubsequences = function(S) {
    let n = S.length;
    let dp = new Array(n).fill(0).map(x => new Array(n).fill(0));
    const kMod = 1000000007;
    for (let i = 0; i < n; i++) dp[i][i] = 1;
    for (let i = n - 1; i >= 0; i--) {
        for (let j = i + 1; j < n; j++) {
            if (S[i] !== S[j]) {
                dp[i][j] += dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1];
            } else {
                dp[i][j] = dp[i + 1][j - 1] * 2;
                let lo = i + 1, hi = j - 1;
                while (lo <= hi && S[lo] !== S[i]) lo++;
                while (lo <= hi && S[hi] !== S[i]) hi--;
                if (lo > hi) dp[i][j] += 2;
                else if (lo === hi) dp[i][j] += 1;
                else dp[i][j] -= dp[lo + 1][hi - 1];
            }
            dp[i][j] = (dp[i][j] + kMod) % kMod;//dp[i][j]有可能是负数，必须 + Kmod变正
        }
    }
    return dp[0][n - 1];
};
```
---

## [create maximum number](https://leetcode.com/problems/create-maximum-number/description/)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/321-ep107-2.png)

> 最后的topK是由 nums1 的 top i 和 nums2 的 top k - i merge 而成
> `maxNumber(nums1, nums2, k) = max{maxNumber(maxNumber(nums1, i), maxNumber(nums2, k - i))}`
> 从 一个数组挑选topK with relative order 很聪明，用到栈
> merge 的时候不是单纯比较队首元素大小，而是比较队列大小

```javascript
var maxNumber = function(nums1, nums2, k) {
    let maxResult = [];
    for (let i = 0; i <= k; i++) {
        if (i > nums1.length || k - i > nums2.length) continue;
        let result = mergeMaxNum(getMaxNum(nums1, i), getMaxNum(nums2, k - i));
        maxResult = result > maxResult ? result: maxResult;
    }
    return maxResult;
};

function getMaxNum(nums, k) {
    let toPop = nums.length - k;
    let result = [];
    for (let num of nums) {
        while (result.length > 0 && num > result[result.length - 1] && toPop > 0) {
            result.pop();
            toPop--;
        }
        result.push(num);
    }
    return result.slice(0, k);
}

function mergeMaxNum (nums1, nums2) {
    let i = 0, j = 0;
    let result = [];
    while (i < nums1.length || j < nums2.length) {
        result.push(pick1(nums1, i, nums2, j) ? nums1[i++] : nums2[j++]);
    }
    return result;
}

function pick1(nums1, s1, nums2, s2) {
    for (let i = s1; i < nums1.length; i++) {
        let j = s2 + i - s1;
        if (j >= nums2.length) return true;
        if (nums1[i] < nums2[j]) return false;
        if (nums1[i] > nums2[j]) return true;
    }
    return false;
}
```
---
## [Edit Distance](https://leetcode.com/problems/edit-distance/description/)

`一遍过` `dfs->dp`

1. dfs + mem
> `editDist(i, j)` 表示 `word1[i:]` and `word2[j:]` 的edit distance.
> 首先考虑edge case， 当其中一个为空怎么办
> 其次考虑都不为空的情况下，首字母一样怎么办，看`word1[i + 1:]` and `word2[j + 1:]`
> 然后首字母不一样, 分三种情况，增，删，改，分别对应不同的sub problem

2. dp
> 和dfs思路一样，不过是从前向后扫描，最后结果为`dp[m][n]`
> `dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]);` 可以看出dp的过程不仅依赖于上一行，同时也依赖于本行的前一个元素。 所以，在计算本行的时候，为了不覆盖上一行的结果，可以在本行独立开出一个数组用来存放本行结果，这样就不用担心覆盖问题了。

```javascript
var minDistance = function(word1, word2) {
    let m = word1.length, n = word2.length;
    let cache = new Array(m).fill(0).map(x => new Array(n).fill(-1));

    function editDist(i, j) {
        if (i === m) return n - j;
        if (j === n) return m - i;
        if (cache[i][j] !== -1) return cache[i][j];
        if (word1[i] === word2[j]) cache[i][j] = editDist(i + 1, j + 1);
        else cache[i][j] = 1 + Math.min(editDist(i + 1, j), editDist(i, j + 1), editDist(i + 1, j + 1));
        return cache[i][j];
    }

    return editDist(0, 0);
};

minDistance = function(word1, word2) {
    let m = word1.length, n = word2.length;
    // let dp = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(0));
    let dp = new Array(n + 1).fill(0);
    // for (let i = 1; i <= m; i++) dp[i][0] = i;
    // for (let j = 1; j <= n; j++) dp[0][j] = j;
    for (let j = 1; j <= n; j++) dp[j] = j;

    for (let i = 1; i <= m; i++) {
        let tmp = new Array(n + 1).fill(0);
        tmp[0] = i;
        for (let j = 1; j <= n; j++) {
            // if (word1[i - 1] === word2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            if (word1[i - 1] === word2[j - 1]) tmp[j] = dp[j - 1];

            // else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]);
            else tmp[j] = 1 + Math.min(dp[j - 1], tmp[j - 1], dp[j]);
        }
        dp = tmp;
    }
    return dp[n];

};
```
---
## [knight probability in chess board](https://leetcode.com/problems/knight-probability-in-chessboard/description/)

`有思路` `不熟` `概率dp` `matrix dp`

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/688-ep79.png)

1. recursion + mem
> `getProb(i, j, step)` 表示当前在(i,j) 还需要走step 步之后留在棋盘内的概率。
> 每走一步的概率是 `1/8` 如果这步出界，那么留在棋盘概率为0，如果不出界，那么就看下一个子问题的概率了.
> edge case是步数用完，那么100%留在棋盘内，概率为1.
> time: O(K * N  ^ 2) . 自由度为3
> space: O(K * N ^ 2)
2. dp
>  转换为计数问题，dp[k][i][j] 表示在k步之后，能从`r,c`走到 `(i, j)`的可能路径个数。
>  统计k步之后，所有可能在棋盘内部的路径个数 除以 `8 ^ k`
>  space: O(N ^ 2) , 可以不管k .

```javascript
var knightProbability = function(N, K, r, c) {
    let cache = new Map();
    const outOfBound = (i, j) => i < 0 || i >= N || j < 0 || j >= N;
    function getProb(i, j, step) {
        if (step === K) return 1;
        let key = `${i},${j},${step}`;
        if (cache.has(key)) return cache.get(key);
        let prob = 0;
        for (let [x, y] of [[i - 1, j + 2], [i - 2, j + 1], [i - 1, j - 2], [i - 2, j - 1],
                            [i + 1, j + 2], [i + 2, j + 1], [i + 1, j - 2], [i + 2, j - 1]]) {
            if (outOfBound(x, y)) continue;
            prob += (1 / 8) *  getProb(x, y, step + 1);
        }
        cache.set(key, prob);
        return prob;
    }
    return getProb(r, c, 0);
};

knightProbability = function(N, K, r, c) {
    const outOfBound = (i, j) => i < 0 || i >= N || j < 0 || j >= N;
    let dp = new Array(N).fill(0).map(x => new Array(N).fill(0));
    dp[r][c] = 1;
    //build dp array
    for (let k = 0; k < K; k++) {
        let tmp = new Array(N).fill(0).map(x => new Array(N).fill(0));
        for (let i = 0; i < N; i++) {
            for (let j = 0; j < N; j++) {
                for (let [x, y] of [[i - 1, j + 2], [i - 2, j + 1], [i - 1, j - 2], [i - 2, j - 1],
                            [i + 1, j + 2], [i + 2, j + 1], [i + 1, j - 2], [i + 2, j - 1]]) {
                    if (outOfBound(x, y)) continue;
                    tmp[i][j] += dp[x][y];
                }
            }
        }
        dp = tmp;
    }
    //cnt probability
    let total = 0;
    for (let i = 0; i < N; i++)
        for (let j = 0; j < N; j++)
            total += dp[i][j];
    return total / Math.pow(8, K);
};
```
---
## [valid parenthesis string](https://leetcode.com/problems/valid-parenthesis-string/description/)

1. brute force
> 将 * 展开成所有可能的情况 `3 ^ k` (左括号，右括号，空), k 为 * 数量，对每种情况做判断
> time: O(N * 3 ^ k)

2. brute force + cache
> `valid(l, r, i)` 表示 检查到 `s[i:]` 已经有 l 个左括号, r 个右括号的时候是不是合法括号.
> 当前状态合法的依据是 `l >= r`, edge case 是 `i === n` 以及 `l < r`
> c 取不同值链接到不同子问题

3. 分类讨论合法情况
> 左右对称，看中间是否合法
> 随机分成两块，看看两块是否分别合法

4. count
> * 不展开，而是可作为 ( 或者 ) 来增加需要匹配的左括号的最大和最小值.
> 在扫描过程中，需要匹配的左括号个数的最大值不能为负数，这样即使 * 全部为 ( , 右括号个数还是多出来.
> we can never have less than 0 open left brackets. `minLeft = Math.max(0, minLeft);`
> For example, if we have string ``(***)`, then as we parse each symbol, the set of possible values for the balance is `[1] for '('; [0, 1, 2] for '(*'; [0, 1, 2, 3] for '(**';`
> 如果最后minLeft > 0 说明即使所有*都展开成右括号，都无法匹配完所有左括号

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/678-ep78.png)

```javascript
var checkValidString = function(s) {
    let n = s.length;
    let cache = new Map();
    function valid(l, r, i) {
        if (i === n) return l === r;
        if (l < r) return false;
        let key = `${l},${r},${i}`;
        if (cache.has(key)) return cache.get(key);
        let c = s[i];
        if (c === '(')
            cache.set(key, valid(l + 1, r, i + 1));
        else if (c === ')')
            cache.set(key, valid(l, r + 1, i + 1));
        else
            cache.set(key, valid(l + 1, r, i + 1) || valid(l, r + 1, i + 1) || valid(l, r, i + 1));
        return cache.get(key);
    }
    return valid(0, 0, 0);
};

checkValidString = function(s) {
    let n = s.length;
    let cache = new Array(n).fill(0).map(x => new Array(n).fill(null));
    function valid(i, j) {
        if (i > j) return true;
        if (i === j) return s[i] === '*';
        if (cache[i][j] !== null) return cache[i][j];
        cache[i][j] = false;
        if ((s[i] === '(' || s[i] === '*') &&
            (s[j] === ')' || s[j] === '*') && valid(i + 1, j - 1)) {
            cache[i][j] = true;
        }
        for (let k = i; k < j; k++) {
            if (valid(i, k) && valid(k + 1, j)) {
                cache[i][j] = true;
                break;
            }
        }
        return cache[i][j];
    }
    return valid(0, n - 1);
};

checkValidString = function(s) {
    let n = s.length;
    if (n === 0) return true;
    let dp = new Array(n).fill(0).map(x => new Array(n).fill(false));
    for (let i = 0; i < n; i++) dp[i][i] = s[i] === '*';
    for (let i = n - 1; i >= 0; i--) {
        for (let j = i + 1; j < n; j++) {
            if ((s[i] === '(' || s[i] === '*') &&
            (s[j] === ')' || s[j] === '*')) {
                if (j === i + 1 || dp[i + 1][j - 1]) {//bug.
                    dp[i][j] = true;
                    continue;
                }
            }
            for (let k = i; k < j; k++) {
                if (dp[i][k] && dp[k + 1][j]) {
                    dp[i][j] = true;
                    break;
                }
            }
        }
    }
    return dp[0][n - 1];
};

checkValidString = function(s) {
    let minLeft = 0, maxLeft = 0;
    for (let c of s) {
        if (c === '(') {
            minLeft++;
            maxLeft++;
        } else if (c === ')') {
            minLeft--;
            maxLeft--;
        } else {
            minLeft--;
            maxLeft++;
        }
        if (maxLeft < 0) return false;
        minLeft = Math.max(0, minLeft);
    }
    return minLeft === 0;
};
```
---
## [strange printer](https://leetcode.com/problems/strange-printer/description/)

`无思路` `字符串dp` `转换子问题`

1. 观察递归关系
> 字符串 `s[i:j]` 最后一个字符 `s[j]` 至少要耗费一次打印，我们想充分利用这次打印，让其覆盖尽可能多的字符.
> 向前寻找和最后一个字符相同的字符 s[k], 可以在打印子串s[i:k]的时候顺便也打印最后一个字符，随意问题就转移成 `s[i:k]` 和 `s[k + 1: j - 1]` 这两个子问题上
> time: O(N ^ 3)
> space: O(N ^ 2)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/664-ep66.png)

```javascript
var strangePrinter = function(s) {
    let n = s.length;
    let cache = new Array(n).fill(0).map(x => new Array(n).fill(-1));
    function cnt(i, j) {
        if (i > j) return 0;
        if (cache[i][j] !== -1) return cache[i][j];

        let ans = cnt(i, j - 1) + 1;
        for (let k = i; k < j; k++) {
            if (s[k] === s[j]) {
                ans = Math.min(ans, cnt(i, k) + cnt(k + 1, j - 1));
            }
        }
        cache[i][j] = ans;
        return ans;
    }
    return cnt(0, n - 1);
};

strangePrinter = function(s) {
    let n = s.length;
    if (n === 0) return 0;//bug
    let dp = new Array(n).fill(0).map(x => new Array(n).fill(Infinity));
    for (let i = n - 1; i >= 0; i--) {
        for (let j = i; j < n; j++) {
            if (j === i) {
                dp[i][j] = 1;
                continue;
            }
            //j > i
            dp[i][j] = dp[i][j - 1] + 1;
            for (let k = i; k < j; k++) {
                if (s[k] === s[j]) {
                    let x = k + 1 <= j - 1 ? dp[k + 1][j - 1] : 0;//bug
                    dp[i][j] = Math.min(dp[i][j], dp[i][k] + x);
                }
            }
        }
    }
    return dp[0][n - 1];
};
```

---

## [Range Sum Query mutable](https://leetcode.com/problems/range-sum-query-mutable/description/)

`新概念` `可以消化` `Fenwick tree`

1. binary indexed tree. Query `O(lgn)` , update `O(lgn)`
> 基本上直接使用Fenwick tree来计算prefix sum
> 注意更新的时候要update nums的值，因为下次计算diff的时候要和更新完的值比较。
> 注意nums的index和Fenwick tree内部的index之间的mapping.

```javascript
var NumArray = function(nums) {
    let n = nums.length;
    this.nums = nums;
    this.sums = new BIT(n);
    for (let i = 1; i <= n; i++) this.sums.update(i, nums[i - 1]);
};

NumArray.prototype.update = function(i, val) {
    this.sums.update(i + 1, val - this.nums[i]);
    this.nums[i] = val;
};

NumArray.prototype.sumRange = function(i, j) {
    return this.sums.query(j + 1) - this.sums.query(i);
};
```
---
## [Range Sum Query 2D - Immutable](https://leetcode.com/problems/range-sum-query-2d-immutable/description/)

`Choke` `matrix sum` `dp`

1. preprocessing `O(m * n)`  + regionQuery `O(1)`
> 预先处理好以 (i, j) 为右下角的matrix sum ，即`dp[i][j]` , 那么就可以再更加其算出以 (i', j')为左上角，(i, j)为右下角的matrix sum。`sum[i][j] = dp[i][j] - dp[i' - 1][j] - dp[i][j' - 1] + dp[i' - 1][j' - 1]`
> 还是dp[m + 1][n + 1] 好啊，避免很多edge case

```javascript
var NumMatrix = function(matrix) {
    let m = matrix.length, n = m === 0 ? 0 : matrix[0].length;
    this.dp = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(0));
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            this.dp[i][j] = matrix[i - 1][j - 1] + this.dp[i - 1][j] + this.dp[i][j - 1] - this.dp[i - 1][j - 1];
        }
    }
};

NumMatrix.prototype.sumRegion = function(row1, col1, row2, col2) {
    return this.dp[row2 + 1][col2 + 1] - this.dp[row1][col2 + 1] - this.dp[row2 + 1][col1] + this.dp[row1][col1];
};
```
---

## [Range Sum Query 2D - Mutable](https://leetcode.com/problems/range-sum-query-2d-mutable/description/)

1. 预处理以(0,0)左上到(i, j) 右下的matrix sum
> 好处是sumQuery 很快 `O(1)`
> 坏处是 update `O(n ^ 2)` 不适合update 频繁的操作
2. 预处理以(0, j) 为上到 (i, j)为下的col sum
> sumQuery变成 `O(n)` 但是 update `O(m)`
3. Fenwick tree 2d
```javascript
var NumMatrix = function(matrix) {
    this.matrix = matrix;
    let m = matrix.length, n = m === 0 ? 0 : matrix[0].length;
    this.m = m;
    this.n = n;
    let colSum = new Array(n).fill(0).map(x => new Array(m + 1).fill(0));
    for (let j = 0; j < n; j++) {
        for (let i = 1; i <= m; i++) {
            colSum[j][i] = colSum[j][i - 1] + matrix[i - 1][j];
        }
    }
    this.colSum = colSum;

};

NumMatrix.prototype.update = function(row, col, val) {
    let [m, n, matrix, colSum] = [this.m, this.n, this.matrix, this.colSum];
    for (let i = row + 1; i <= m; i++) colSum[col][i] += val - matrix[row][col];
    matrix[row][col] = val;
};

NumMatrix.prototype.sumRegion = function(row1, col1, row2, col2) {
    let sum = 0;
    let colSum = this.colSum;
    for (let j = col1; j <= col2; j++) {
        sum += colSum[j][row2 + 1] - colSum[j][row1];
    }
    return sum;
};
// Fenwick Tree
var NumMatrix = function(matrix) {
    let m = matrix.length, n = m === 0 ? 0: matrix[0].length;
    this.sums = new BIT(m, n);
    this.matrix = matrix;
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            this.sums.update(i + 1, j + 1, matrix[i][j]);
        }
    }
};

NumMatrix.prototype.update = function(row, col, val) {
    this.sums.update(row + 1, col + 1, val - this.matrix[row][col]);
    this.matrix[row][col] = val;
};

NumMatrix.prototype.sumRegion = function(row1, col1, row2, col2) {
    return this.sums.query(row2 + 1, col2 + 1) - this.sums.query(row2 + 1, col1) - this.sums.query(row1, col2 + 1) + this.sums.query(row1, col1);
};
```
---
## [Maximal Square](https://leetcode.com/problems/maximal-square/solution/)

1. bruteforce
>  Whenever a 1 is found, we try to find out the largest square that can be formed including that 1.
>  we move diagonally (right and downwards)
>  check whether all the elements of that row and column are 1 or not.
>  Time: O((mn) ^ 2)
>  Space: O(1)

2. dp
`dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1`
> up, left, diag have all been calculated when we reach `(i, j)`
> we can use matrix to hold the dp result because we only need matrix[i][j] untouched, which is gauranteed.
> Time: O(mn)
> Space: O(1)

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/221-ep62-1.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/221-ep62-2.png)
![3](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/221-ep62-3.png)
![4](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/221-ep62-4.png)

```javascript
var maximalSquare = function(matrix) {
    let maxSize = 0;
    let m = matrix.length, n = m === 0 ? 0 : matrix[0].length;
    for (let i = 0; i < m; i++)
        for (let j = 0; j < n; j++) {
            if (matrix[i][j] === '0') matrix[i][j] = 0;
            else {
                let left = j - 1 >= 0 ? matrix[i][j - 1] : 0,
                    up = i - 1 >= 0 ? matrix[i - 1][j] : 0,
                    diag = (i - 1 >= 0 && j - 1 >= 0) ? matrix[i - 1][j - 1] : 0;
                matrix[i][j] = Math.min(left, up, diag) + 1;
            }
            maxSize = Math.max(maxSize, matrix[i][j]);
        }
    return maxSize * maxSize;
};
```
---
## [longest increasing subsequence](https://leetcode.com/problems/longest-increasing-subsequence/description/)

1. `dp O(n^2) maxEnding`
> Scan through the nums array, calculate the LIS ending at index `i` by comparing `nums[i]` with the previous nums .

2. `dp + binary search`
> Scan through the nums array, this time, instead of checking previous maxEnding one by one (which is not sorted), we check if we can create a longer increasing subseq .
> To leverage binary search, we need to maintain a sorted state array.

> `tails` is an array storing the smallest tail of all increasing subsequences with length `i+1` in `tails[i]` .
why smallest tail ? for the ease of extending/updating the increasing sub sequence.

> For each incomming element, we binary search the tails array to see which increasing subseq we can update, if the incomming element is bigger than all the tails, than we found a longer increasing subseq.

> if `tails[i-1] < x <= tails[i]`, update `tails[i]`.

```javascript
var lengthOfLIS = function(nums) {
    let dp = new Array(nums.length).fill(1);
    let maxLen = 0;
    for (let i = 0; i < nums.length; i++) {
        for (let j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                dp[i] = Math.max(dp[i], 1 + dp[j]);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }
    return maxLen;
};

// [10, 9, 2, 5, 3, 7, 101, 18]
// tails: []
// tails: [10]
// tails: [9]
// tails: [2]
// tails: [2, 5]
// tails: [2, 3]
// tails: [2, 3, 7]
// tails: [2, 3, 7, 101]
// tails: [2, 3, 7, 18]
var lengthOfLIS = function(nums) {
    let n = nums.length;
    if (n === 0) return 0;
    let dp = [nums[0]];//smallest num with LIS len == 1 is nums[0];
    for (let i = 1; i < n; i++) {
        let num = nums[i];
        let pos = binSearch(dp, num);//find the first element > num, update it's value
        dp[pos] = num;
    }

    function binSearch(arr, target) {
        let lo = 0, hi = arr.length - 1;
        while (lo < hi) {
            let mid = lo + ~~((hi - lo) / 2);
            if (arr[mid] < target) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        return arr[lo] >= target ? lo : lo + 1;
    }

    return dp.length;
};
```


---
## [number of longest increasing subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/description/)

`有思路` `不熟练` `数组dp`

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/673-ep56.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/673-ep56-2.png)

```javascript
var findNumberOfLIS = function(nums) {
    let n = nums.length;
    if (n === 0) return 0;
    let len = new Array(n).fill(1);
    let cnts = new Array(n).fill(1);

    let longest = 1;
    for (let i = 1; i < n; i++) {
        for (let j = 0; j < i; j++) {
            if (nums[i] <= nums[j]) continue;
            if (len[j] + 1 > len[i]) {
                len[i] = len[j] + 1;
                cnts[i] = cnts[j];
            } else if (len[j] + 1 === len[i]) {
                cnts[i] += cnts[j];
            }
        }
        longest = Math.max(len[i], longest);
    }

    let sum = 0;
    for (let i = 0; i < n; i++) {
        if (len[i] === longest) sum += cnts[i];
    }
    return sum;
};
```
---
## [Different ways to add parenthesis](https://leetcode.com/problems/different-ways-to-add-parentheses/description/)

`有思路` `不熟` `结果组合dp`

> 以每个operator作为分割符号，递归求解子问题
> 用cache记录下 input[i:j] 的解，不需要重复计算
> 注意number的位数可能不止一位。

```javascript
var diffWaysToCompute = function(input) {
    let n = input.length;
    if (n === 0) return 0;

    const isOpr = x => new Set(['+', '-', '*']).has(x);
    const plus = (x, y) => x + y;
    const minus = (x, y) => x - y;
    const mul = (x, y) => x * y;

    let cache = new Array(n).fill(0).map(x => new Array(n).fill(null));

    function result(i, j) {
        if (cache[i][j] !== null) return cache[i][j];
        let res = [];
        for (let k = i + 1; k < j; k++) {
            if (isOpr(input[k])) {
                let left = result(i, k - 1), right = result(k + 1, j);
                let fn = input[k] === '+' ? plus : (input[k] === '-') ? minus : mul;
                res = [...res, ...cartProd(left, right, fn)];
            }
        }
        cache[i][j] = res.length === 0 ? [Number(input.slice(i, j + 1))]: res;
        return cache[i][j];
    }

    function cartProd(A, B, fn) {
        let res = [];
        for (let x of A) {
            for (let y of B) {
                res.push(fn(x, y));
            }
        }
        return res;
    }

    return result(0, n - 1);
};
```

---
## [Word Break](https://leetcode.com/problems/word-break/description/)

`一遍过` `有印象` `dfs + mem / bfs + mem / dp`

1. Bruteforce (backtracking) `O(n ^ n)`
> we check every possible prefix in the dict, if it's found in the dict, then we recursively call the `wordBreak` with the remaining substring. If we can find any prefix in the dict that has a breakable substring, then the whole string can be wordbreak.
> Time complexity : consider the worst case where s = "aaaaaa" and every prefix of s is present in the dict, then the recursion tree has height of n (chop of one letter at a level) and a branch factor of n (has n prefix to cut).
2. Recursion with memorization `O(n ^ 2)`
> we were calling the recursive function multiple times for a particular string
e.g. dict = ['le', 'et', 'leet'] , path 'le' + 'et' === 'leet'.
> Time complexity: We have `O(n)` distinct subproblems, and we need `O(n)` to solve each one.
3. Dynamic programming `O(n ^ 2)`
4. BFS `O(n ^ 2)`
> 基本上和backtracking一样，bfs的节点用i来表示 `s[0:i)` can word break. 每一步都看看有没有prefix能够帮忙reach到下一层节点，用que来存储下一层的node.
> 一共有 n 层，每一层耗时 O(n) 来遍历所有prefix。

```javascript
var wordBreak = function(s, wordDict) {
    wordDict = new Set(wordDict);
    let n = s.length;
    let cache = new Map(); //key: starting index value: true/false

    const canBreak = i => {
        if (i === n) return true;
        if (cache.has(i)) return cache.get(i);
        cache.set(i, false);
        for (let j = i + 1; j <= n; j++) {
            let word = s.slice(i, j);
            if (!wordDict.has(word)) continue;
            if (canBreak(j)) {
                cache.set(i, true);
                break;
            }
        }
        return cache.get(i);
    };

    return canBreak(0);
};

wordBreak = function(s, wordDict) {
    wordDict = new Set(wordDict);
    let n = s.length;
    if (n === 0) return false;
    let dp = new Array(n + 1).fill(false); //s[0: i) can word break
    dp[0] = true;
    for (let i = 1; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            let word = s.slice(j, i);
            if (wordDict.has(word) && dp[j]) {
                dp[i] = true;
                break;
            }
        }
    }
    return dp[n];
};

wordBreak = function(s, wordDict) {
    wordDict = new Set(wordDict);
    let n = s.length;
    let visited = new Array(n + 1).fill(false);
    visited[0] = true;
    let que = [0];
    while (que.length > 0) {
        let i = que.shift();
        for (let j = i + 1; j <= n; j++) {
            let word = s.slice(i, j);
            if (wordDict.has(word) && !visited[j]) {
                que.push(j);
                visited[j] = true;
            }
        }
    }
    return visited[n];
};
```
---
## [word break II](https://leetcode.com/problems/word-break-ii/description/)

> 先dp算出parents的index结构，只有合法的substring才有parents
> 然后dfs parents的index结构
> Time: O(n ^ 2 + dfsParents tree)
> 相比较直接dfs求解，搜索的树的大小小了很多。

```javascript
var wordBreak = function(s, wordDict) {
    let n = s.length;
    wordDict = new Set(wordDict);
    let parents = new Array(n + 1).fill(0).map(x => []);
    let dp = new Array(n + 1).fill(false);
    dp[0] = true;
    for (let i = 1; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            let prefix = s.slice(j, i);
            if (wordDict.has(prefix) && dp[j]) {
                dp[i] = true;
                parents[i].push(j);
            }
        }
    }
    let results = [];
    function dfs(start, path) {
        if (start === 0) {
            results.push([...path].reverse().join(' '));
            return;
        }
        for (let p of parents[start]) {
            path.push(s.slice(p, start));
            dfs(p, path);
            path.pop();
        }
    }
    dfs(n, []);
    return results;
};
```
---
## [regular expression matching](https://leetcode.com/problems/regular-expression-matching/description/)

> 关键是 `*` 这里要带走一个preceding char，所以如果是计划递归从前到后扫描的时候要记得look one step further，先讨论 `p[j + 1] === '*'` 的情况
> edge case : j === n , i === m 要分别讨论
> bottom up dp 也是先初始化edge case. 然后再两边都有字符的情况下放心开始dp

```javascript
var isMatch = function(s, p) {
    let m = s.length, n = p.length;
    let cache = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(null));
    function match(i, j) {
        if (j === n) return i === m;
        if (i === m) return j < n - 1 && p[j + 1] === '*' && match(i, j + 2);
        if (cache[i][j] !== null) return cache[i][j];
        let firstMatch = p[j] === '.' || p[j] === s[i];
        if (j < n - 1 && p[j + 1] === '*') {
            cache[i][j] = match(i, j + 2) || (firstMatch && match(i + 1, j));
        } else {
            cache[i][j] = firstMatch && match(i + 1, j + 1);
        }
        return cache[i][j];
    }
    return match(0, 0);
};

var isMatch = function(s, p) {
    let m = s.length, n = p.length;
    let dp = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(false));
    dp[0][0] = true;
    for (let i = 1; i <= n; i++) dp[0][i] = i > 1 && p[i - 1] === '*' && dp[0][i - 2];
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (p[j - 1] === '*') {
                dp[i][j] = dp[i][j - 2] || ((p[j - 2] === '.' || p[j - 2] === s[i - 1]) && dp[i - 1][j]);
            } else {
                dp[i][j] = (p[j - 1] === '.' || p[j - 1] === s[i - 1]) && dp[i - 1][j - 1];
            }
        }
    }
    return dp[m][n];
};
```
---
## [wild card matching](https://leetcode.com/problems/wildcard-matching/description/)

> The difference is that: the * in this problem can match any sequence independently, while the * in Regex Matching would only match duplicates, if any, of the character prior to it.

```javascript
var isMatch = function(s, p) {
    let m = s.length, n = p.length;
    let cache = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(null));
    function match(i, j) {
        if (j === n) return i === m;
        if (i === m) return p[j] === '*' && match(i, j + 1);
        if (cache[i][j] !== null) return cache[i][j];

        let firstMatch = p[j] === '?' || p[j] === s[i];
        if (p[j] === '*') {
            cache[i][j] = match(i, j + 1) || match(i + 1, j);
        } else {
            cache[i][j] = firstMatch && match(i + 1, j + 1);
        }
        return cache[i][j];
    }
    return match(0, 0);
};

isMatch = function(s, p) {
    let m = s.length, n = p.length;
    let dp = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(false));
    dp[0][0] = true;
    for (let i = 1; i <= n; i++) dp[0][i] = p[i - 1] === '*' && dp[0][i - 1];
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (p[j - 1] === '*') {
                dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
            } else {
                dp[i][j] = (p[j - 1] === '?' || p[j - 1] === s[i - 1]) && dp[i - 1][j - 1];
            }
        }
    }
    return dp[m][n];
};
```
---
## [palindrom substring](https://leetcode.com/problems/palindromic-substrings/description/)

`Denifition of Palindrom`
> `s[i: j] is palin === (s[i] === s[j] && s[i+1: j - 1] is palin)`
> edge case:
> by our definition, if s[i: j) contains less than 2 elements, it's a palindrom.

```javascript
var countSubstrings = function(s) {
    let n = s.length;
    let cache = new Array(n).fill(0).map(x => new Array(n).fill(null));

    function isPalin(i, j) {
        if (i >= j) return true;
        if (cache[i][j] !== null) return cache[i][j];
        cache[i][j] = s[i] === s[j] && isPalin(i + 1, j - 1);
        return cache[i][j];
    }

    let cnt = 0;
    for (let i = 0; i < n; i++) {
        for (let j = i; j < n; j++) {
            if (isPalin(i, j)) cnt++;
        }
    }
    return cnt;
};

var countSubstrings = function(s) {
    let n = s.length;
    let dp = new Array(n).fill(0).map(x => new Array(n).fill(false));
    let cnt = 0;
    for (let i = n - 1; i >= 0; i--) {
        for (let j = i; j < n; j++) {
            if (j === i) {
                dp[i][j] = true;
            } else {
                dp[i][j] = s[i] === s[j] && (j === i + 1 || dp[i + 1][j - 1]);
            }
            cnt += dp[i][j] ? 1 : 0;
        }
    }
    return cnt;
};

var countSubstrings = function(s) {
    let cnt = 0;
    for (let i = 0; i < s.length; i++) cnt += countFrom(s, i, i);
    for (let i = 0; i < s.length - 1; i++) cnt += countFrom(s, i, i + 1);
    return cnt;
};

function countFrom(s, lo, hi) {
    if (s[lo] !== s[hi]) return 0;
    let cnt = 0; //s[lo] === s[hi] , itself is a palindrome
    while (lo >= 0 && hi < s.length && s[lo] === s[hi]) {
        cnt++;
        lo--;
        hi++;
    }
    return cnt;
}
```
