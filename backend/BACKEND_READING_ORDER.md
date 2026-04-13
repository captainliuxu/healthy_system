# Backend Reading Order

## 1. 这份文档解决什么问题

这份文档不是再讲“每个文件叫什么”，而是告诉你:

1. 现在应该按什么顺序读代码
2. 每一层是怎么串起来的
3. 一个请求从进入后端到最终落库，完整经过了哪些文件

如果你现在容易出现这种情况:

1. 文件都认识
2. 但串不起来
3. 不知道为什么这个接口会跑到那个 service
4. 不知道为什么 token 能识别当前用户

那这份文档就是给你的。

---

## 2. 先建立一个最重要的整体认知

当前这个后端，按第二阶段已经完成的正式主链路来看，核心调用顺序可以先记成:

`main -> api/router -> 路由函数 -> deps 取依赖 -> service 处理业务 -> model 落数据库 -> schema 整理输入输出 -> response 返回统一结果`

这句话建议你先背下来。

因为你以后读大多数接口，本质上都是在读这条链。

---

## 3. 最推荐的读代码顺序

如果你现在要从零开始把这个后端读懂，推荐顺序如下。

## 第 1 轮: 先看骨架，不碰具体业务

先读这几个文件:

1. `app/main.py`
2. `app/api/router.py`
3. `app/core/config.py`
4. `app/db/session.py`
5. `app/core/response.py`
6. `app/core/exception.py`

这一轮的目标只有一个:

先搞懂“这个后端怎么启动、怎么连库、怎么回响应、怎么统一处理错误”。

### 这一轮你应该读懂什么

#### `app/main.py`

你要读懂:

1. FastAPI 应用是在哪里创建的
2. CORS 是在哪里加的
3. 总路由是在哪里挂的
4. 全局异常处理器是在哪里注册的

#### `app/api/router.py`

你要读懂:

1. 总路由只负责汇总，不写业务
2. 当前正式接入的是哪些路由

#### `app/core/config.py`

你要读懂:

1. 配置不是写死在每个文件里
2. 项目通过 `settings` 统一读取配置
3. `.env` 里的内容是怎么进入 Python 的

#### `app/db/session.py`

你要读懂:

1. 数据库引擎怎么建
2. Session 怎么建
3. FastAPI 路由里拿到的 `db: Session` 从哪来

#### `app/core/response.py`

你要读懂:

1. 为什么很多接口都不是自己手写 JSON
2. 为什么它们统一用 `success_response`

#### `app/core/exception.py`

你要读懂:

1. 业务异常为什么不是直接 `raise ValueError`
2. 为什么接口报错时还能返回统一 JSON 结构

---

## 第 2 轮: 看认证主链路

先读这几个文件:

1. `app/schemas/auth.py`
2. `app/core/security.py`
3. `app/api/deps.py`
4. `app/models/user.py`
5. `app/services/auth_service.py`
6. `app/api/routes/auth.py`

这一轮的目标是:

搞懂注册、登录、JWT 鉴权这条链。

### 这一轮你应该读懂什么

#### `app/schemas/auth.py`

你要读懂:

1. 注册接口到底收什么字段
2. `confirm_password` 是怎么校验的
3. 登录成功后 token 长什么样

#### `app/core/security.py`

你要读懂:

1. 明文密码是怎么变成哈希的
2. 登录时怎么校验密码
3. token 是怎么生成的
4. token 是怎么解析的

#### `app/api/deps.py`

你要读懂:

1. 受保护接口为什么能识别当前用户
2. `get_current_user` 具体做了什么
3. `get_current_active_user` 比 `get_current_user` 多做了什么

#### `app/models/user.py`

你要读懂:

1. 用户表里到底存了哪些字段
2. 为什么存的是 `password_hash` 而不是明文密码

#### `app/services/auth_service.py`

你要读懂:

1. 注册时怎么做唯一性校验
2. 登录时怎么验证账号密码
3. 登录成功后怎么签发 token

#### `app/api/routes/auth.py`

你要读懂:

1. HTTP 请求是怎么进入业务层的
2. 为什么登录接口拿的是 `OAuth2PasswordRequestForm`
3. 为什么注册接口返回的是统一响应，而登录接口直接返回 token

---

## 第 3 轮: 看用户和档案主链路

先读这几个文件:

1. `app/schemas/user.py`
2. `app/schemas/profile.py`
3. `app/models/profile.py`
4. `app/services/user_service.py`
5. `app/services/profile_service.py`
6. `app/api/routes/users.py`
7. `app/api/routes/profiles.py`

这一轮的目标是:

搞懂用户本人信息和 profile 信息是怎么被管理的。

### 这一轮你应该读懂什么

#### `app/schemas/user.py`

你要读懂:

1. 用户读取结构长什么样
2. 用户更新时允许改哪些字段

#### `app/schemas/profile.py`

你要读懂:

1. Profile 创建时允许传哪些字段
2. Profile 更新时为什么很多字段都是可选的
3. Profile 返回结构长什么样

#### `app/models/profile.py`

你要读懂:

1. `Profile` 表里有哪些字段
2. `user_id` 为什么是唯一的
3. 为什么当前是一个用户对应一个 profile

#### `app/services/user_service.py`

你要读懂:

1. 为什么更新用户信息前还要再查唯一性
2. 为什么 service 层不直接信任前端传来的值

#### `app/services/profile_service.py`

你要读懂:

1. 当前用户怎么拿到自己的 profile
2. 为什么同一个用户不能重复创建多个 profile

#### `app/api/routes/users.py`

你要读懂:

1. 为什么 `GET /users/me` 能直接知道“我是谁”
2. 为什么 `PUT /users/me` 需要同时注入 `db` 和 `current_user`

#### `app/api/routes/profiles.py`

你要读懂:

1. 为什么路径是 `/profiles/me`
2. 为什么 profile 接口必须带当前登录用户

---

## 第 4 轮: 最后再看数据库迁移

先读这几个文件:

1. `app/models/__init__.py`
2. `app/db/base.py`
3. `alembic/env.py`
4. `alembic/versions/cf9c75bd0f5c_create_users_and_profiles.py`

这一轮的目标是:

搞懂“代码里的模型是怎么变成数据库里的表”的。

### 这一轮你应该读懂什么

#### `app/models/__init__.py`

你要读懂:

1. 当前正式模型集合有哪些
2. 为什么模型要有统一导出入口

#### `app/db/base.py`

你要读懂:

1. Alembic 为啥要通过它拿模型
2. 为什么不是随便扫描整个项目

#### `alembic/env.py`

你要读懂:

1. Alembic 是怎么拿数据库地址的
2. Alembic 是怎么拿 `Base.metadata` 的

#### `alembic/versions/*.py`

你要读懂:

1. 数据库真正被创建成了什么样
2. 当前已经正式迁移过哪些表

---

## 4. 推荐你先不要急着读哪些文件

按你现在的理解阶段，不建议一开始就钻这些文件:

1. `app/db/models/record.py`
2. `app/db/models/conversation.py`
3. `app/db/models/message.py`
4. `app/db/models/proactive_window.py`
5. `app/db/models/proactive_log.py`
6. `app/schemas/chat.py`
7. `app/schemas/conversation.py`
8. `app/schemas/proactive.py`
9. `app/schemas/record.py`
10. `app/repositories/profile_repo.py`
11. `app/models/record.py`

原因不是这些文件不重要，而是:

1. 它们不属于当前第二阶段正式主链路
2. 你现在先读它们，很容易把正式代码和草稿代码混在一起
3. 一旦混起来，你就会产生“为什么这个文件有，但接口里看不到”的困惑

所以正确顺序是:

先把第二阶段正式链路吃透，再看这些后续阶段文件。

---

## 5. 现在把正式主链路串一遍

下面我用几个最典型的接口，把整条链串一遍。

---

## 6. 例子一: 注册接口是怎么跑起来的

对应接口:

`POST /api/v1/auth/register`

### 第一步: 请求进入路由

文件:

`app/api/routes/auth.py`

这里做的事:

1. 接收注册请求体 `UserRegisterRequest`
2. 注入数据库会话 `db`
3. 调用 `auth_service.register(db, payload)`

### 第二步: 业务逻辑进入 service

文件:

`app/services/auth_service.py`

这里做的事:

1. 查用户名是否重复
2. 查邮箱是否重复
3. 查手机号是否重复
4. 调用 `hash_password` 对密码做哈希
5. 创建 `User` 对象
6. `db.add -> db.commit -> db.refresh`

### 第三步: 落到 ORM 模型

文件:

`app/models/user.py`

这里定义了用户表结构，也就是最终数据库里 `users` 表长什么样。

### 第四步: 返回统一响应

文件:

1. `app/api/routes/auth.py`
2. `app/core/response.py`
3. `app/schemas/common.py`

这里做的事:

1. 把 `User` ORM 对象转成 `UserRead`
2. 用 `success_response` 包成统一 JSON 壳

最终你会拿到:

1. `code`
2. `message`
3. `data`

---

## 7. 例子二: 登录接口是怎么跑起来的

对应接口:

`POST /api/v1/auth/login`

### 第一步: 路由接收表单

文件:

`app/api/routes/auth.py`

这里做的事:

1. 用 `OAuth2PasswordRequestForm` 接收用户名密码
2. 调用 `auth_service.login`

### 第二步: service 做认证

文件:

`app/services/auth_service.py`

这里做的事:

1. 按用户名查用户
2. 用 `verify_password` 校验密码
3. 检查用户是否激活
4. 调用 `create_access_token`

### 第三步: security 生成 JWT

文件:

`app/core/security.py`

这里做的事:

1. 构造 token payload
2. 设置过期时间
3. 用密钥和算法签发 JWT

最终返回给前端的是:

1. `access_token`
2. `token_type`

---

## 8. 例子三: `GET /users/me` 为什么能知道当前是谁

对应接口:

`GET /api/v1/users/me`

### 第一步: 路由声明依赖

文件:

`app/api/routes/users.py`

这里写了:

```python
current_user: User = Depends(get_current_active_user)
```

意思是:

这个接口执行前，必须先把“当前激活用户”解析出来。

### 第二步: 进入 `get_current_active_user`

文件:

`app/api/deps.py`

这里做的事:

1. 先调用 `get_current_user`
2. 再检查 `is_active`

### 第三步: 进入 `get_current_user`

文件:

`app/api/deps.py`

这里做的事:

1. 从请求里拿 Bearer token
2. 调用 `decode_access_token`
3. 从 token 里解析出 `sub`
4. 用 `sub` 去数据库查对应的 `User`

### 第四步: security 负责解 token

文件:

`app/core/security.py`

这里做的事:

1. 校验 token 签名
2. 校验 token 是否过期
3. 返回 payload

所以 `GET /users/me` 能知道“当前是谁”，本质原因不是魔法，而是:

1. token 里有用户 id
2. `deps.py` 把它解析出来
3. 再查数据库拿到当前用户对象

---

## 9. 例子四: `POST /profiles/me` 是怎么落库的

对应接口:

`POST /api/v1/profiles/me`

### 第一步: 路由接收请求体

文件:

`app/api/routes/profiles.py`

这里做的事:

1. 接收 `ProfileCreate`
2. 注入 `db`
3. 注入 `current_user`
4. 调用 `profile_service.create_for_user`

### 第二步: service 处理业务规则

文件:

`app/services/profile_service.py`

这里做的事:

1. 先检查当前用户是否已经有 profile
2. 如果有，抛业务异常
3. 如果没有，创建新的 `Profile`
4. 把 `user_id=current_user.id` 绑定进去

### 第三步: ORM 模型负责映射到表

文件:

`app/models/profile.py`

这里定义数据库里 `profiles` 表怎么存。

### 第四步: 返回 `ProfileRead`

文件:

1. `app/api/routes/profiles.py`
2. `app/schemas/profile.py`

这里把 ORM 对象转成响应结构，再套上统一返回壳。

---

## 10. 推荐你真正开始读代码时的执行方式

最稳的方法不是“看一堆文件名”，而是“带着问题读”。

推荐你这样读:

### 第一步

先问自己:

“这个接口入口在哪?”

然后去 `app/api/routes/` 里找。

### 第二步

再问自己:

“这个接口真正的业务逻辑在哪?”

然后去 `app/services/` 里找。

### 第三步

再问自己:

“这个 service 操作的是哪张表?”

然后去 `app/models/` 里找。

### 第四步

再问自己:

“请求体和响应体长什么样?”

然后去 `app/schemas/` 里找。

### 第五步

再问自己:

“这个接口为什么知道当前用户是谁?”

然后回到:

1. `app/api/deps.py`
2. `app/core/security.py`

---

## 11. 如果你只想最快读懂当前正式链路

那你可以只读下面这一组:

1. `app/main.py`
2. `app/api/router.py`
3. `app/core/config.py`
4. `app/db/session.py`
5. `app/core/response.py`
6. `app/core/exception.py`
7. `app/core/security.py`
8. `app/api/deps.py`
9. `app/models/user.py`
10. `app/models/profile.py`
11. `app/schemas/auth.py`
12. `app/schemas/user.py`
13. `app/schemas/profile.py`
14. `app/services/auth_service.py`
15. `app/services/user_service.py`
16. `app/services/profile_service.py`
17. `app/api/routes/auth.py`
18. `app/api/routes/users.py`
19. `app/api/routes/profiles.py`
20. `alembic/env.py`
21. `alembic/versions/cf9c75bd0f5c_create_users_and_profiles.py`

这一组文件吃透了，你对当前后端的理解就已经很扎实了。

---

## 12. 一句话总结推荐阅读路线

最稳的顺序不是按目录机械往下翻，而是按下面这条逻辑链去读:

`启动入口 -> 全局规则 -> 鉴权 -> 用户模型 -> Profile 模型 -> service -> route -> migration`

等你把这条第二阶段正式主链路读顺了，再去看 `record / conversation / proactive`，你就不会乱。
