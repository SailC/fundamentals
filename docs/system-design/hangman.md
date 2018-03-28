# hangman

### hangman front end v.s backend

* 前端存放UI code
* 前端通过ajax call和后台发送action
* 后台收到action之后改变game的status，（根据结果对错）
* 前端根据return body 来改变UI element

### 如果游戏还没完，如何检测到用户掉线

* 如果 server 超过30s没有检测到客户端的request，用户被视为掉线。
* 修改user table中的status to be offline
* all the game data is saved in the db
* when the user come back online, session id -> user id -> game id -> resume
* session, user & game data can be cached for fast query.

### 如何实现 用户登录

```
user table
----------
id
email
username
passwd
status
score
game_id
```

```
session log file
----------
id
user_id
expire_at
```

* When user registered, UI will ask user to provide email/usrname and password. A verification email will be sent to the email specified by the user, clicking the link will post a confirmation message to the server and a user table entry with the credentials will be created.  

* When user loging with the correct credential, an session id is associated with him and user status is changed to online.  

### 可以查看历史游戏结果

```
game table
-----------
id
user_id
result
target_word
cur_word
```

### start a new game

* create a new game table entry and randomly select a word from a word list. The words can be precomputed in the cache randomly every now and then, and pick a random word each time.
* update the game table with the new word, user_id, and return the game status for UI to render.

* [rest API format](https://github.com/donnemartin/system-design-primer#rpc-and-rest-calls-comparison)

* the returned game status can be applied to react status to render the UI.

* load game, guess action all return game status.

### storage

* the structure of the game data is pretty much self-contained, a document data store should be enough.

* user id -> {game_id1, game_id2}

### leader board

* use message broker to stream the result of game to the leaderboard service which aggregate the user statistics over time and update the leaderboard table in real-time

### payment

* better use 3rd party service to interact with financial transactions.
* SQL db for ACID transactions

### scale

* memcache (shard by userId , consistent hashing)
* document database (shard by userid, consistent hashing)
