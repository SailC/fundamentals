# 专题

classic question for each topic.

## Fenwick Tree / Binary Indexed Tree

Fenwick Tree is mainly designed for solving **Single Point Update Range Sum** problems, e.g, the sum between i-th & j-th element while the values of the elements are **mutable** .

Init the tree (including building all prefix sums) takes `O(nlgn)`

Update the value of an element takes `O(lgn)`

Query the range sum takes `O(lgn)`

Space complexity `O(n)`

![Motivation](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/sp3-1.png)
![Update & Query](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/sp3-1.png)

```javascript
class BIT {
  constructor(size) {
    this.sums = new Array(size + 1).fill(0);
    this.size = size + 1;
  }

  update(i, delta) {
    while (i < this.size) {
      this.sums[i] += delta;
      i += this._lowbit(i);
    }
  }

  query(i) {
    let sum = 0;
    while (i > 0) {
      sum += this.sums[i];
      i -= this._lowbit(i);
    }
    return sum;
  }

  _lowbit(x) {
    return x & (-x);
  }
}
```

## 2D binary indexed tree. Query `O(lgm lgn)`, update `O(lgm lgn)`

```javascript
class BIT {
  constructor(m, n) {
    this.sums = new Array(m + 1).fill(0).map(x => new Array(n + 1).fill(0));
    this.m = m + 1;
    this.n = n + 1;
  }

  update(row, col, delta) {
    for (let i = row; i < this.m; i += this._lowbit(i)) {
      for (let j = col; j < this.n; j += this._lowbit(j)) {
        this.sums[i][j] += delta;
      }
    }
  }

  query(row, col) {
    let sum = 0;
    for (let i = row; i > 0; i -= this._lowbit(i)) {
      for (let j = col; j > 0; j -= this._lowbit(j)) {
        sum += this.sums[i][j];
      }
    }
    return sum;
  }

  _lowbit(x) {
    return x & (-x);
  }
}
```

## Time/Space Complexity of Recursion Function

- [花花酱说递归](http://zxi.mytechroad.com/blog/sp/time-space-complexity-of-recursion-functions-sp4/)

- [花花酱说时间复杂度](http://zxi.mytechroad.com/blog/sp/input-size-v-s-time-complexity/)

- ![Input & time complexity](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/sp2.png)

- 10: O(n!) permutation
- 15: O(2^n) combination
- 50: O(n^4) DP
- 200: O(n^3) DP, all pairs shortest path
- 1,000: O(n^2) DP, all pairs, dense graph
- 1,000,000: O(nlogn), sorting-based (greedy), heap, divide & conquer
- 1,000,000: O(n), DP, graph traversal / topological sorting (V+E), tree traversal
- INT_MAX: O(sqrt(n)), prime, square sum
- INT_MAX: O(logn), binary search
- INT_MAX: O(1) Math
