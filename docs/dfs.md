## [flood-fill](https://leetcode.com/problems/flood-fill/description/)
`一遍过` `回味` `dfs/bfs`

1. bfs
> 产生儿子的同时就要change color，不然siblings 会产生相同的儿子，造成duplicates
2. dfs
> 用color来做判重，原路径（或者其他已经被访问过的节点）的颜色都已经改变，可用来免费判重

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/733-ep116.png)

```javascript
var floodFill = function(image, sr, sc, newColor) {
    let m = image.length, n = m === 0 ? 0 : image[0].length;
    if (m === 0 || n === 0) return image;

    const inRange = (i, j) => i >= 0 && i < m && j >= 0 && j < n;
    let color = image[sr][sc];

    function bfs(sr, sc, newColor) {

        if (newColor === color) return;

        let que = [[sr, sc]];
        image[sr][sc] = newColor;
        while (que.length > 0) {
            let [i, j] = que.shift();
            for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
                if (inRange(x, y) && image[x][y] === color) {
                    image[x][y] = newColor;
                    que.push([x, y]);
                }
            }
        }
    }

    bfs(sr, sc, newColor);
    return image;
};

floodFill = function(image, sr, sc, newColor) {
    let m = image.length, n = m === 0 ? 0 : image[0].length;
    if (m === 0 || n === 0 || newColor === image[sr][sc]) return image;
    let color = image[sr][sc];
    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    (function dfs(i, j) {
        if (outOfBound(i, j) || image[i][j] !== color) return;
        image[i][j] = newColor;
        for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) dfs(x, y);
    })(sr, sc);
    return image;
};
```
---
## [number of islands](https://leetcode.com/problems/number-of-islands/description/)
`一遍过` `回味` `dfs/bfs`

1. `dfs`
for each remaining island, flood it with `bfs` or `dfs`. Each flood destroy a island. count how many island you can flood.

2. `careful about bfs`
The idea is that if you push all the pair into a queue before mark the grid, the same points might be pushed into queue by the siblings multiple times. `dfs` doesn't have this problem as the adj nodes are flooded immediately. A better way to solve this is to `mark & flood`, so that the runtime is still O(m * n)

```javascript
var numIslands = function(grid) {
    if (grid === null || grid.length === 0) return 0;
    let m = grid.length, n = grid[0].length;

    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    function dfs(i, j) {
        if (outOfBound(i, j) || grid[i][j] === '0') return;
        grid[i][j] = '0';
        for (let [x, y] of [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]) dfs(x, y);
    }

    function bfs(i, j) {
        let que = [[i, j]];
        grid[i][j] = '0';
        while (que.length > 0) {
            let [i, j] = que.pop();
            for (let [x, y] of [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]]) {
                if (outOfBound(x, y) || grid[x][y] === '0') continue;
                grid[x][y] = '0';
                que.push([x, y]);
            }
        }
    }

    let cnt = 0;
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === '1') {
                cnt++;
                // dfs(i, j);
                bfs(i, j);
            }
        }
    }
    return cnt;
};
```
---
## [Max area of islands](https://leetcode.com/problems/max-area-of-island/description/)

`一遍过` `回味` `dfs/bfs`

```javascript
var maxAreaOfIsland = function(grid) {
    let m = grid.length, n = m === 0 ? 0 : grid[0].length;
    let maxArea = 0;

    const outOfBound = (i, j) => i < 0 || i >= m || j < 0 || j >= n;

    function dfs(i, j) {
        if (outOfBound(i, j) || grid[i][j] === 0) return 0;
        grid[i][j] = 0;
        let cnt = 1;
        for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
            cnt += dfs(x, y);
        }
        return cnt;
    }

    function bfs(i, j) {
        let que = [[i, j]];
        grid[i][j] = 0;
        let cnt = 0;
        while (que.length > 0) {
            let [i, j] = que.shift();
            cnt++;
            for (let [x, y] of [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]) {
                if (outOfBound(x, y) || grid[x][y] === 0) continue;
                grid[x][y] = 0;
                que.push([x, y]);
            }
        }
        return cnt;
    }

    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === 1) {
                //maxArea = Math.max(maxArea, dfs(i, j));
                maxArea = Math.max(maxArea, bfs(i, j));
            }
        }
    }
    return maxArea;
};
```

---
## [Friend Circles](https://leetcode.com/problems/friend-circles/description/)

`一遍过` `回味` `dfs/bfs` `UF`

1. dfs
> The given matrix can be viewed as the Adjacency Matrix of a graph. our problem reduces to the problem of finding the number of connected components in an undirected graph.
> from the graph, we can see that the components which are connected can be reached starting from any single node of the connected group. Thus, to find the number of connected components, we start from every node which isn't visited right now and apply DFS starting with it. We increment the countcount of connected components for every new starting node
> Time: `O(n^2)`
2. bfs
> Same idea. We increment the countcount of connected components whenever we need to start off with a new node as the root node for applying BFS which hasn't been already visited.
> Time: `O(n^2)` Each cell in adj matrix is visited once.
3. UF
> We traverse over all the nodes of the graph. For every node traversed, we traverse over all the nodes directly connected to it and assign them to a single group which is represented by their parentparent node
> At the end, we find the number of groups, or the number of parent nodes.
> Time: `O(n ^3)` We traverse over the complete matrix once. Union and find operations take O(n)O(n) time in the worst case.

```javascript
var findCircleNum = function(M) {
    let n = M.length;
    let cnt = 0;
    let visited = new Array(n).fill(false);

    function dfs(i) {
        if (visited[i]) return;
        visited[i] = true;
        for (let j = 0; j < n; j++) {
            if (j !== i && M[i][j]) dfs(j);
        }
    }

    function bfs(i) {
        let que = [i];
        visited[i] = true;
        while (que.length > 0) {
            let i = que.shift();
            for (let j = 0; j < n; j++) {
                if (j !== i && M[i][j] && !visited[j]) {
                    visited[j] = true;
                    que.push(j)
                }
            }
        }
    }

    for (let i = 0; i < n; i++) {
        if (!visited[i]) {
            //dfs(i);
            bfs(i);
            cnt++;
        }
    }
    return cnt;
};

var findCircleNum = function(M) {
    let uf = new UF(M.length);
    for (let i = 0; i < M.length; i++) {
        for (let j = 0; j < M[i].length; j++) {
            if (i < j && M[i][j] === 1) {
                uf.union(i, j);
            }
        }
    }
    return uf.size;
};
```
