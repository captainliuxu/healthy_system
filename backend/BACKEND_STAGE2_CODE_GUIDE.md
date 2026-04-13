# Backend Stage2 Code Guide

## 1. 这份文档是干什么的

这份文档的目标是:

1. 帮你从“第二阶段已经完成”的视角看懂当前 `backend/`
2. 告诉你每个目录现在负责什么
3. 告诉你每个文件现在大概是干什么的
4. 帮你区分哪些文件是当前正式链路，哪些只是后续阶段草稿

这份文档默认你的理解基线是:

1. 第一阶段已经完成基础骨架
2. 第二阶段已经完成 `User / Auth / Profile`
3. 第三阶段你正在做，但当前仓库里还存在一些未完全接入的草稿文件

所以阅读这份文档时，你要优先把注意力放在:

1. 当前正式主链路
2. 第二阶段已经打通的文件

而不是一开始就钻进后续阶段草稿。

---

## 2. 先看 `backend/` 根目录

当前 `backend/` 根目录的主要内容可以按下面几类来理解。

### 2.1 项目主目录

| 路径 | 当前作用 |
| --- | --- |
| `app/` | 后端真正的业务代码主目录，最重要 |
| `alembic/` | 数据库迁移目录，用来管理表结构变更 |
| `tests/` | 测试目录，目前基本还是空的 |

### 2.2 环境和配置文件

| 路径 | 当前作用 |
| --- | --- |
| `requirements.txt` | 后端依赖清单 |
| `alembic.ini` | Alembic 的配置文件 |

### 2.3 本地数据库文件

| 路径 | 当前作用 |
| --- | --- |
| `healthy_system.db` | 当前主 SQLite 数据库 |
| `review_smoke.db` | 某次调试或冒烟测试生成的数据库 |
| `review_smoke2.db` | 某次调试或冒烟测试生成的数据库 |
| `review_smoke3.db` | 某次调试或冒烟测试生成的数据库 |

这些 `.db` 文件都不是“代码”，它们只是本地运行时生成出来的数据文件。

### 2.4 说明文档

| 路径 | 当前作用 |
| --- | --- |
| `前后端对接规范_阶段二.md` | 第二阶段接口联调用说明 |
| `目录分工说明.txt` | 目录职责说明，属于项目内部辅助文档 |

### 2.5 开发环境产物

| 路径 | 当前作用 |
| --- | --- |
| `.venv/` | Python 虚拟环境，不属于业务代码 |
| `__pycache__/` | Python 缓存目录，可以忽略 |

---

## 3. 你现在应该先把 `backend/` 看成三层

为了便于理解，你可以先把整个后端想成三层:

### 第一层: 基础骨架层

主要包括:

1. `app/main.py`
2. `app/core/`
3. `app/db/`
4. `alembic/`

这一层负责:

1. 应用启动
2. 配置读取
3. 数据库连接
4. 异常处理
5. 统一响应
6. 数据库迁移

### 第二层: 第二阶段正式业务层

主要包括:

1. `app/models/user.py`
2. `app/models/profile.py`
3. `app/schemas/auth.py`
4. `app/schemas/user.py`
5. `app/schemas/profile.py`
6. `app/services/auth_service.py`
7. `app/services/user_service.py`
8. `app/services/profile_service.py`
9. `app/api/routes/auth.py`
10. `app/api/routes/users.py`
11. `app/api/routes/profiles.py`

这一层负责:

1. 用户注册登录
2. JWT 鉴权
3. 用户信息查看与修改
4. Profile 的创建、查看、修改

### 第三层: 后续阶段草稿层

主要包括:

1. `app/models/record.py`
2. `app/db/models/record.py`
3. `app/db/models/conversation.py`
4. `app/db/models/message.py`
5. `app/db/models/proactive_*`
6. `app/schemas/chat.py`
7. `app/schemas/conversation.py`
8. `app/schemas/proactive.py`
9. `app/schemas/record.py`
10. `app/repositories/profile_repo.py`

这些文件说明:

1. 它们表示你项目已经开始往第三阶段、第四阶段、主动提醒方向预留结构
2. 但按“第二阶段已经完成”的视角，它们大多不是当前正式主链路
3. 所以你读代码时，不要一开始就把它们当作当前系统已经完全接通的功能

---

## 4. `app/` 目录总览

`app/` 是整个后端最重要的目录。

你可以先记住它里面几个子目录的职责:

| 目录 | 作用 |
| --- | --- |
| `app/api/` | HTTP 接口层，收请求、回响应 |
| `app/core/` | 全局规则层，放配置、异常、响应、安全 |
| `app/db/` | 数据库层，放会话、Base、草稿模型 |
| `app/models/` | 当前正式 ORM 模型层 |
| `app/schemas/` | Pydantic 数据结构层 |
| `app/services/` | 业务逻辑层 |
| `app/repositories/` | 辅助数据访问层，目前只出现了一个草稿仓储 |

一句话记忆:

1. `api` 负责进出 HTTP
2. `schemas` 负责数据长什么样
3. `services` 负责业务逻辑
4. `models` 负责数据库表映射
5. `db` 负责数据库连接和迁移入口
6. `core` 负责全局规则

---

## 5. `app/` 根目录文件说明

### `app/main.py`

作用:

1. 创建 FastAPI 应用对象
2. 注册 CORS 中间件
3. 挂载总路由 `api_router`
4. 注册全局异常处理器

这是整个后端服务的启动入口。

你以后运行:

```powershell
uvicorn app.main:app --reload
```

本质上就是从这里启动。

### `app/__init__.py`

作用:

1. 把 `app/` 变成 Python 包
2. 目前基本没有业务逻辑

这种文件你可以理解成“包标记文件”。

---

## 6. `app/api/` 目录说明

`app/api/` 是 HTTP 接口层。

它的职责是:

1. 接收请求
2. 注入依赖
3. 调用 service
4. 返回统一响应

你可以把它理解成:

“后端对外说话的那一层”

### 6.1 `app/api/deps.py`

作用:

1. 提供数据库依赖 `get_db`
2. 提供当前用户依赖 `get_current_user`
3. 提供当前激活用户依赖 `get_current_active_user`

这是第二阶段最关键的接口依赖文件之一。

因为从第二阶段开始，后端很多接口都需要知道:

1. 这次请求是谁发来的
2. 这个用户是否合法
3. 这个用户是否还处于激活状态

### 6.2 `app/api/router.py`

作用:

1. 汇总所有子路由
2. 让 `main.py` 只需要挂一个总路由

当前正式接入的主要路由是:

1. `health`
2. `auth`
3. `users`
4. `profiles`

这说明从第二阶段视角看，当前正式主链路集中在:

1. 基础健康检查
2. 注册登录
3. 用户信息
4. 用户 Profile

### 6.3 `app/api/routes/health.py`

作用:

1. 提供服务存活检查接口
2. 提供数据库连通性检查接口

这是第一阶段、第二阶段都很重要的一个辅助路由。

它不是业务功能，但对排查问题非常有用。

### 6.4 `app/api/routes/auth.py`

作用:

1. 提供注册接口
2. 提供登录接口

这是第二阶段最核心的入口之一。

你所有受保护接口要能工作，前提都是先完成:

1. 注册
2. 登录
3. 拿到 JWT token

### 6.5 `app/api/routes/users.py`

作用:

1. 提供 `GET /users/me`
2. 提供 `PUT /users/me`

这是第二阶段“用户本人信息”接口。

它关注的是账号信息本身，比如:

1. 用户名
2. 邮箱
3. 手机号

### 6.6 `app/api/routes/profiles.py`

作用:

1. 提供 `POST /profiles/me`
2. 提供 `GET /profiles/me`
3. 提供 `PUT /profiles/me`

这是第二阶段“用户健康档案”接口。

它关注的是用户画像和健康基础信息，比如:

1. 姓名
2. 年龄
3. 身高
4. 体重
5. 既往史

---

## 7. `app/core/` 目录说明

`app/core/` 放的是全局规则。

也就是说，凡是“不是某个具体业务专属，而是整个项目都要遵守的东西”，一般都放这里。

### 7.1 `app/core/config.py`

作用:

1. 统一读取环境变量
2. 定义项目配置对象 `Settings`
3. 提供全局可复用的 `settings`

它里面主要管理的配置包括:

1. 项目名
2. 调试开关
3. API 前缀
4. 数据库地址
5. JWT 配置
6. CORS 配置
7. LLM 基础配置

这是整个项目的配置中心。

### 7.2 `app/core/response.py`

作用:

1. 提供统一成功响应 `success_response`
2. 提供统一错误响应 `error_response`

它的意义是:

让你的后端接口返回格式保持一致。

第二阶段之后，大多数正常接口最终都应该走这里。

### 7.3 `app/core/exception.py`

作用:

1. 定义业务异常 `BusinessException`
2. 定义 HTTP 异常、校验异常、通用异常的处理方式
3. 统一把异常转成标准 JSON 响应

这是“后端不要把错误胡乱抛给前端”的关键文件。

你可以把它理解成:

“整个项目的错误出口”

### 7.4 `app/core/security.py`

作用:

1. 密码哈希
2. 密码校验
3. JWT 创建
4. JWT 解析
5. OAuth2 token 依赖定义

这是第二阶段鉴权体系的核心文件。

登录为什么能发 token，受保护接口为什么能识别 token，关键都在这里。

---

## 8. `app/db/` 目录说明

`app/db/` 负责数据库底层相关内容。

### 8.1 `app/db/session.py`

作用:

1. 创建数据库引擎
2. 定义 SQLAlchemy 的 `Base`
3. 定义 `SessionLocal`
4. 提供 `get_db` 依赖

这是数据库连接层的核心文件。

后面所有 service 真正访问数据库时，拿到的 `db: Session` 都是从这里来的。

### 8.2 `app/db/base.py`

作用:

1. 作为 Alembic 扫描模型的统一入口
2. 导入当前正式 ORM 模型

按你当前仓库状态看，它主要导入的是:

1. `User`
2. `Profile`

这说明从第二阶段视角看，Alembic 当前正式关注的模型还是这两个。

### 8.3 `app/db/models/`

这个目录目前更像“后续阶段草稿模型区”。

也就是说:

1. 这里已经出现了一些未来业务的草稿表
2. 但它们目前不一定真正接入正式主链路

#### `app/db/models/record.py`

作用:

1. 早期的 Record 草稿模型
2. 使用的是另一套字段设计思路

从当前第二阶段视角看，它不是正式主链路的一部分。

#### `app/db/models/conversation.py`

作用:

1. 会话模块的早期草稿模型
2. 说明项目已经开始为聊天结构做准备

但从第二阶段视角看，它还没有真正进入正式路由链路。

#### `app/db/models/message.py`

作用:

1. 消息模块的早期草稿模型
2. 用于为后续聊天消息落库预留结构

目前也不是第二阶段正式链路的一部分。

#### `app/db/models/proactive_window.py`

作用:

1. 主动提醒时段窗口的草稿模型
2. 为后续“主动关怀 / 提醒策略”做预留

#### `app/db/models/proactive_log.py`

作用:

1. 主动提醒触发日志的草稿模型
2. 为后续提醒记录、触发原因记录做预留

---

## 9. `app/models/` 目录说明

`app/models/` 是当前正式 ORM 模型目录。

只要一个模型在这里，并且被 `app/models/__init__.py` 和 `app/db/base.py` 正式导入，通常它才算当前主链路的正式模型。

### 9.1 `app/models/user.py`

作用:

定义用户表 `users`。

这是第二阶段最核心的模型之一。

它关注的是账号身份本身，包括:

1. 用户名
2. 邮箱
3. 手机号
4. 密码哈希
5. 是否激活
6. 创建和更新时间

### 9.2 `app/models/profile.py`

作用:

定义用户档案表 `profiles`。

这是第二阶段另一个核心模型。

它关注的是用户画像和健康档案信息，包括:

1. 姓名
2. 年龄
3. 性别
4. 身高
5. 体重
6. 慢病史
7. 过敏史
8. 紧急联系人
9. 备注

### 9.3 `app/models/record.py`

作用:

这是你当前仓库里已经出现的 Record 正式模型草稿。

但要注意:

按当前第二阶段已经完成、第三阶段未完全接入的状态看，它还不属于稳定主链路。

判断依据主要是:

1. 当前正式 API 路由里还没有 records 路由
2. `app/models/__init__.py` 目前还没有把它正式导入
3. `app/db/base.py` 目前也没有把它正式导入

所以你读代码时，要把它理解成:

“已经开始进入第三阶段，但还没彻底并入主链路的文件”

### 9.4 `app/models/__init__.py`

作用:

1. 汇总当前正式模型
2. 给别的地方统一导出模型

你当前仓库里，这个文件主要还是把:

1. `User`
2. `Profile`

作为当前主模型导出。

这再次说明第二阶段正式链路依然是当前最稳定的部分。

---

## 10. `app/schemas/` 目录说明

`app/schemas/` 负责定义 Pydantic 数据结构。

简单理解:

1. 请求体长什么样
2. 响应体长什么样
3. 某些中间结构长什么样

都在这里定义。

### 10.1 `app/schemas/common.py`

作用:

1. 定义通用响应壳 `ApiResponse`

这个文件很重要，因为你的很多接口最终都会返回:

1. `code`
2. `message`
3. `data`

它是统一返回结构的核心。

### 10.2 `app/schemas/auth.py`

作用:

1. 定义注册请求体
2. 定义 token 结构
3. 定义 token payload 结构

这是第二阶段认证功能的数据结构文件。

### 10.3 `app/schemas/user.py`

作用:

1. 定义用户读取结构 `UserRead`
2. 定义用户更新结构 `UserUpdate`

### 10.4 `app/schemas/profile.py`

作用:

1. 定义 `ProfileCreate`
2. 定义 `ProfileUpdate`
3. 定义 `ProfileRead`

这是第二阶段 Profile 模块最重要的 schema 文件。

### 10.5 `app/schemas/record.py`

作用:

这是 Record 模块的草稿 schema 文件。

它表示你已经开始为第三阶段准备数据结构，但从当前第二阶段视角看，它还不是稳定主链路。

### 10.6 `app/schemas/conversation.py`

作用:

这是会话和消息读取结构的早期草稿 schema。

它说明项目已经开始往聊天方向扩展，但还没有形成正式第四阶段完整链路。

### 10.7 `app/schemas/chat.py`

作用:

这是聊天请求和聊天响应的草稿结构。

它的存在说明:

你后面大概率会做 `/chat` 之类的接口。

但从当前第二阶段视角看，它还不是正式接通的主链路文件。

### 10.8 `app/schemas/proactive.py`

作用:

这是主动提醒相关的数据结构草稿。

包括:

1. 主动提醒窗口
2. 主动触发请求
3. 主动触发日志读取结构

它明显属于更后面的阶段。

---

## 11. `app/services/` 目录说明

`app/services/` 是业务逻辑层。

你可以把它理解成:

“真正决定业务规则怎么跑的一层”

路由层一般不应该堆太多业务逻辑，所以第二阶段最重要的业务都放在这里。

### 11.1 `app/services/auth_service.py`

作用:

1. 注册用户
2. 检查用户名/邮箱/手机号唯一性
3. 验证登录
4. 登录后签发 token

这是第二阶段认证业务的核心 service。

### 11.2 `app/services/user_service.py`

作用:

1. 更新当前用户的基本信息
2. 做用户名/邮箱/手机号的唯一性校验

### 11.3 `app/services/profile_service.py`

作用:

1. 按用户查 profile
2. 为用户创建 profile
3. 获取当前用户 profile
4. 更新当前用户 profile

这是第二阶段 Profile 模块最核心的 service。

---

## 12. `app/repositories/` 目录说明

### `app/repositories/profile_repo.py`

作用:

这是一个比较早期的数据访问层尝试。

它做的是:

1. create
2. get_by_id
3. list
4. update
5. delete

但按你当前第二阶段正式主链路看，它并没有成为当前主业务流程的核心组成部分。

也就是说:

你现在正式运行的第二阶段逻辑，主要还是:

`route -> service -> ORM`

而不是:

`route -> service -> repository -> ORM`

所以读代码时，这个文件先知道它存在即可，不要一开始就把精力放在它身上。

---

## 13. `alembic/` 目录说明

`alembic/` 负责数据库迁移。

你可以把它理解成:

“数据库结构版本管理区”

### 13.1 `alembic/env.py`

作用:

1. 告诉 Alembic 到哪里去拿数据库连接
2. 告诉 Alembic 到哪里去拿模型元数据

这个文件是 Alembic 工作的核心入口。

### 13.2 `alembic/script.py.mako`

作用:

Alembic 生成 migration 文件时使用的模板。

一般情况下你不用主动改它。

### 13.3 `alembic/README`

作用:

Alembic 自带的说明文件。

### 13.4 `alembic/versions/cf9c75bd0f5c_create_users_and_profiles.py`

作用:

这是当前仓库里最重要的一份迁移文件之一。

它说明:

第二阶段真正被 Alembic 正式落库的主要是:

1. `users`
2. `profiles`

这和当前正式主链路完全一致。

---

## 14. `tests/` 目录说明

当前 `tests/` 目录基本还是空的。

这说明:

1. 当前项目主要还是以教学和功能落地为主
2. 自动化测试体系还没有真正铺开

如果你后面继续完善项目，这个目录会变得越来越重要。

---

## 15. 按第二阶段视角，你最该先读哪部分

如果你现在的目标是“先把当前已经稳定的代码读懂”，推荐优先读这几块:

1. `app/main.py`
2. `app/core/config.py`
3. `app/db/session.py`
4. `app/core/response.py`
5. `app/core/exception.py`
6. `app/core/security.py`
7. `app/api/deps.py`
8. `app/models/user.py`
9. `app/models/profile.py`
10. `app/schemas/auth.py`
11. `app/schemas/user.py`
12. `app/schemas/profile.py`
13. `app/services/auth_service.py`
14. `app/services/user_service.py`
15. `app/services/profile_service.py`
16. `app/api/routes/auth.py`
17. `app/api/routes/users.py`
18. `app/api/routes/profiles.py`
19. `app/api/router.py`

这基本就是你第二阶段已经正式打通的后端主链路。

---

## 16. 读代码时你现在最容易混淆的地方

### 16.1 `app/models/` 和 `app/db/models/` 为什么会同时存在

简单说:

1. `app/models/` 是当前正式模型目录
2. `app/db/models/` 更像历史残留或后续草稿区

所以你当前读正式链路时，优先看 `app/models/`。

### 16.2 为什么有 `record.py`、`conversation.py`，但接口里没看到

因为这些文件代表的是后续阶段的准备工作，不等于它们已经正式接入:

1. 路由
2. service
3. Alembic
4. 主入口

所以“文件存在”不等于“功能已经完整可用”。

### 16.3 `ProfileRepository` 为什么有，但 `ProfileService` 没用它

因为当前项目主要走的是更直接的:

`service -> ORM`

这说明项目还处在逐步演进阶段，而不是已经形成严格分层的最终版本。

---

## 17. 一句话总结当前后端状态

如果只按第二阶段完成度来理解，你当前后端最稳定、最值得先读懂的，是这条主链:

`main -> api router -> auth/users/profiles routes -> services -> user/profile models -> db session`

而 `record / conversation / message / proactive` 这些文件，现在更适合被理解成:

“后续阶段已经开始露头，但还没有完全并入当前正式主链路的预研或草稿”
