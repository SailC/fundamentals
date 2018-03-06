# 专题

classic question for each topic.

## Fenwick Tree / Binary Indexed Tree

Fenwick Tree is mainly designed for solving **Single Point Update Range Sum** problems, e.g, the sum between i-th & j-th element while the values of the elements are **mutable** .

Init the tree (including building all prefix sums) takes `O(nlgn)`

Update the value of an element takes `O(lgn)`

Query the range sum takes `O(lgn)`

Space complexity `O(n)`

![Motivation](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/sp3-1.png)
![Update & Query](http://zxi.mytechroad.com/blog/wp-content/uploads/2018/01/sp3-2.png)

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

> BIT只不过是一颗虚拟的树，目的是将部分和存在不同节点里，这种分散的存储便于更新，因为只需要更新
> 一部分节点。BIT根据最低位的1bit将节点和她的parent链接起来
> 2D BIT也是一种partial sum的虚拟映射关系，只不过这个映射过程是二维的，先将行做映射，确定当前节点
> 对应那些行的partial sum之和，然后对于每一行，对列进行映射.

```
节点(4, 4) = sum(matrix[1][1], matrix[1][2], matrix[1][4],
                matrix[2][1], matrix[2][2], matrix[2][4],
                matrix[4][1], matrix[4][2], matrix[4][4],
                )
```

![1](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/304-ep63-1.png)
![2](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/09/304-ep63-2.png)

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
