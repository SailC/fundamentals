## [asteroids collision](https://leetcode.com/problems/asteroid-collision/description/)

`有思路` `stack`

key observation
> output 左半边一定是 -, 右半边一定是+, 否则会碰撞
> 可以假设正陨石都不动，负陨石向左飞。
> time: O(n) 每次至少有一颗陨石爆炸, 所以不会是O(n^2)
1. stack
> 如果是正陨石，入账
> 如果是负陨石，首先看看有没碰撞，没有的话直接入栈
> 否则碰撞到直到碰撞不了为止，期间记录下来看看负陨石有没有爆炸

![thought](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/12/735-ep122-1.png)

```javascript
var asteroidCollision = function(asteroids) {
    let stack = [];
    const top = stack => stack[stack.length - 1];
    const canCollide = stack => !(stack.length === 0 || top(stack) < 0);
    for (let ast of asteroids) {
        if (ast > 0) stack.push(ast);
        else {
            if (!canCollide(stack)) {
                stack.push(ast);
            } else {
                let explode = false;
                while (canCollide(stack)) {
                    if (Math.abs(ast) <= top(stack)) {
                        explode = true;
                        if (Math.abs(ast) === top(stack)) stack.pop();
                        break;
                    }
                    stack.pop();
                }
                if (!explode) stack.push(ast);
            }
        }
    }
    return stack;
};
```
