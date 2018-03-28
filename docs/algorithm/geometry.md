# Geometry

## [construct the rectangle](https://leetcode.com/problems/construct-the-rectangle/description/)

`width * length === area` && `width <= length` => `width * width <= area`
so `for width = 1 -> w * w <= are`

```javascript
var constructRectangle = function(area) {
    let result = [area, 1]; //[length, width]
    for (let width = 1; width * width <= area; width++) {
        if (area % width === 0) {
            let length = ~~(area / width);
            result = [length, width];
        }
    }
    return result;
};
```

---

## [max points on a line](https://leetcode.com/problems/max-points-on-a-line/description/)

![](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/10/149-ep92.png)


```javascript
var maxPoints = function(points) {
    let maxNum = 0;
    const samePoints = (a, b) => a.x === b.x && a.y === b.y;
    for (let i = 0; i < points.length; i++) {
        let dup = 1; // there may be duplicated points, which should be cnt in every line across that point
        let slopCnt = new Map(); //map slop of the line to the number of points in that line
        let localMaxNum = 0;
        for (let j = i + 1; j < points.length; j++) {
            if (samePoints(points[i], points[j])) {
                dup++;
                continue;
            }
            let slop = getSlope(points[i], points[j]);
            slopCnt.set(slop, (slopCnt.get(slop) || 0) + 1);
            localMaxNum = Math.max(localMaxNum, slopCnt.get(slop));
        }
        maxNum = Math.max(maxNum, dup + localMaxNum);
    }
    return maxNum;
};

function getSlope(pointA, pointB) {
    if (pointA.x === pointB.x) return JSON.stringify({x: pointA.x, y: 0});
    if (pointA.y === pointB.y) return JSON.stringify({x: 0, y: pointA.y});
    let dx = pointA.x - pointB.x, dy = pointA.y - pointB.y;
    let d = gcd(dx, dy);
    return JSON.stringify({x: dx / d, y: dy / d});
}

function gcd(m, n) {
    return n === 0 ? m : gcd(n, m % n);
}
```
