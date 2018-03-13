## [my calendar II](https://leetcode.com/problems/my-calendar-ii/description/)
`有思路` `不熟练` `intervals`

- [MyCalendar I](./bst.md#my-calendar-i)

1. double que
> Maintain a list of bookings and a list of double bookings. When booking a new event [start, end), if it conflicts with a double booking, it will have a triple booking and be invalid. Otherwise, parts that overlap the calendar will be a double booking
> 注意，其中dbEvents可以用mycalendarI来代替，但是events是可以overlap的.
> 由于events可以overlap，所以无法继续使用bst来进行二分搜索，直接使用暴力数组来存储event.
> 发现overlap之后用 `{start: Math.max(start, e.start), end: Math.min(end, e.end)}` 计算出overlap 插入dbEvents里面

![thoughts](http://zxi.mytechroad.com/blog/wp-content/uploads/2017/11/731-ep113-1.png)

```javascript
var MyCalendarTwo = function() {
    this.events = [];
    this.dbEvents = [];//db => double booking
};

MyCalendarTwo.prototype.book = function(start, end) {
    const conflictWith = e => !(end <= e.start || start >= e.end);
    for (let e of this.dbEvents) {
        if (conflictWith(e)) return false;
    }
    for (let e of this.events) {
        if (conflictWith(e)) {
            let dbEvent = {start: Math.max(start, e.start), end: Math.min(end, e.end)};
            this.dbEvents.push(dbEvent);
        }
    }
    this.events.push({start: start, end: end});
    return true;
};
```
