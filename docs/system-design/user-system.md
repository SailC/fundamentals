# User system

## Authentication Service

用户是如何实现登陆与保持登陆的？

* 会话表 Session
    * 用户 Login 以后
    * 创建一个 session 对象
    * 并把 session_key 作为 cookie 值返回给浏览器
    * 浏览器将该值记录在浏览器的 cookie 中
    * 用户每次向服务器发送的访问，都会自动带上该网站所有的 cookie
    * 此时服务器检测到cookie中的session_key是有效的，就认为用户登陆了

* 用户 Logout 之后
    * 从 session table 里删除对应数据
    
* Session table 放cache & db.

```
session table
---
session_key string 一个 hash 值，全局唯一，无规律
user_id Foreign key 指向 User Table
expire_at timestamp 什么时候过期
```
