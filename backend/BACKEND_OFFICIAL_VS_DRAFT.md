# Backend Official vs Draft

## 1. 为什么要专门写这份文档

你当前 `backend/` 里有一个很容易让人读乱的现象:

有些文件已经是当前正式主链路的一部分，真正参与:

1. 路由
2. 鉴权
3. 数据库迁移
4. 接口返回

但也有一些文件只是:

1. 后续阶段草稿
2. 预留结构
3. 历史尝试
4. 尚未接入主入口

如果你不先把这两类文件分开，很容易出现下面这些困惑:

1. 为什么这个文件明明存在，但接口里根本用不到
2. 为什么有 `record.py`，却没有对应正式路由
3. 为什么有 `conversation.py`，但数据库迁移里没有它
4. 为什么有 `ProfileRepository`，但正式业务没走 repository 层

这份文档就是专门帮你区分:

哪些是正式主链路，哪些是草稿。

---

## 2. 先定义三个状态

为了便于理解，这里把文件分成三种状态。

### 状态 A: 正式主链路

特点:

1. 已经被当前应用真正用到
2. 路由已挂载
3. 或者已被 service / deps / main / Alembic 正式依赖

你现在读代码时，最应该先关注这一类。

### 状态 B: 正式基础设施

特点:

1. 不直接提供业务接口
2. 但整个项目运行离不开它

比如:

1. 配置
2. 数据库会话
3. 异常处理
4. 统一响应
5. 迁移入口

### 状态 C: 草稿 / 预研 / 未完全接入

特点:

1. 文件存在
2. 但没有完全进入当前稳定主链路
3. 常见于后续阶段预留模块

你现在读代码时，先知道有这类文件就行，不要一开始把它们和正式主链路混在一起。

---

## 3. 当前最稳定的正式主链路文件

下面这些文件，按你现在“第二阶段已经完成”的理解，是最该优先看的。

### 3.1 启动和全局层

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `app/main.py` | 正式主链路 | 应用启动入口 |
| `app/api/router.py` | 正式主链路 | 总路由汇总 |
| `app/core/config.py` | 正式基础设施 | 全局配置中心 |
| `app/core/response.py` | 正式基础设施 | 统一成功/错误响应 |
| `app/core/exception.py` | 正式基础设施 | 全局异常处理 |
| `app/core/security.py` | 正式基础设施 | 密码哈希、JWT 签发和解析 |
| `app/api/deps.py` | 正式基础设施 | 当前用户、数据库依赖注入 |
| `app/db/session.py` | 正式基础设施 | 引擎、Session、Base、get_db |

### 3.2 正式模型层

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `app/models/user.py` | 正式主链路 | 用户表模型 |
| `app/models/profile.py` | 正式主链路 | 用户档案表模型 |
| `app/models/__init__.py` | 正式基础设施 | 当前正式模型统一导出 |
| `app/db/base.py` | 正式基础设施 | Alembic 扫描模型入口 |

### 3.3 正式 schema 层

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `app/schemas/common.py` | 正式主链路 | 通用响应壳 |
| `app/schemas/auth.py` | 正式主链路 | 注册和 token 结构 |
| `app/schemas/user.py` | 正式主链路 | 用户读写结构 |
| `app/schemas/profile.py` | 正式主链路 | Profile 读写结构 |

### 3.4 正式 service 层

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `app/services/auth_service.py` | 正式主链路 | 注册、登录、认证 |
| `app/services/user_service.py` | 正式主链路 | 用户信息更新 |
| `app/services/profile_service.py` | 正式主链路 | Profile 创建、查询、更新 |

### 3.5 正式 route 层

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `app/api/routes/health.py` | 正式主链路 | 服务和数据库健康检查 |
| `app/api/routes/auth.py` | 正式主链路 | 注册、登录 |
| `app/api/routes/users.py` | 正式主链路 | 当前用户信息 |
| `app/api/routes/profiles.py` | 正式主链路 | 当前用户档案 |

### 3.6 正式迁移层

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `alembic/env.py` | 正式基础设施 | 迁移入口 |
| `alembic/versions/cf9c75bd0f5c_create_users_and_profiles.py` | 正式主链路 | 当前真正落库的用户和档案迁移 |

---

## 4. 当前存在但不要先当正式主链路看的文件

下面这些文件不是“没用”，而是你现在读正式代码时，不应该优先把它们当主链路。

---

## 5. Record 相关文件

### `app/models/record.py`

状态:

草稿 / 正在进入第三阶段

为什么说它不是当前第二阶段正式主链路:

1. 当前 `app/models/__init__.py` 没把它正式导出
2. 当前 `app/db/base.py` 没把它正式导入
3. 当前 `app/api/router.py` 还没有 records 路由

怎么理解它:

这是你项目往第三阶段发展的一个正式方向草稿，但按当前稳定运行主链路看，它还没有完全接入。

### `app/schemas/record.py`

状态:

草稿 / 第三阶段预留

说明:

这是 Record 模块的数据结构准备文件，但当前稳定主链路里并没有正式走到这一步。

### `app/db/models/record.py`

状态:

草稿 / 历史分支模型

说明:

它和 `app/models/record.py` 同时存在，很容易把人读晕。  
你现在可以先记住:

1. 当前正式模型目录优先看 `app/models/`
2. `app/db/models/record.py` 不要当成第二阶段主链路文件

---

## 6. Conversation / Message 相关文件

### `app/db/models/conversation.py`

状态:

草稿 / 第四阶段预留

说明:

它说明项目已经开始为聊天会话表做预留。

但它目前不是当前第二阶段正式接口链路的一部分。

### `app/db/models/message.py`

状态:

草稿 / 第四阶段预留

说明:

这是聊天消息表的草稿模型。

它和 `conversation.py` 一样，属于“后续阶段已经露头，但还没接入当前稳定链路”的文件。

### `app/schemas/conversation.py`

状态:

草稿 / 第四阶段预留

说明:

这是会话和消息读取结构的早期定义。

从当前第二阶段视角看，它不是你最该优先读的 schema。

### `app/schemas/chat.py`

状态:

草稿 / 聊天接口预留

说明:

这个文件说明你后面会很可能做:

1. `ChatRequest`
2. `ChatResponse`

但当前并没有真正接入 `/chat` 正式接口。

所以它先理解成“将来会用到的结构草稿”。

---

## 7. 主动提醒相关文件

### `app/db/models/proactive_window.py`

状态:

草稿 / 更后续阶段预留

说明:

它表示后面可能会做“提醒时段窗口”这类功能。

### `app/db/models/proactive_log.py`

状态:

草稿 / 更后续阶段预留

说明:

它表示后面可能会做“提醒触发日志”这类功能。

### `app/schemas/proactive.py`

状态:

草稿 / 更后续阶段预留

说明:

它和上面两个 proactive 模型是同一条未来功能线上的。

当前先不用优先读。

---

## 8. `app/repositories/profile_repo.py` 怎么看

状态:

辅助草稿 / 非当前主业务通路

为什么它容易让人困惑:

1. 目录名看起来很正规
2. 方法也看起来很完整
3. 但当前正式业务其实没有真正依赖它

当前真正的主业务路径主要还是:

`route -> service -> ORM`

而不是:

`route -> service -> repository -> ORM`

所以你可以把它理解成:

一个数据访问层尝试，但不是当前稳定主链路的核心。

---

## 9. 怎么判断一个文件到底是不是当前主链路

你以后可以用下面这套方法自己判断。

### 方法一: 看 `app/api/router.py`

如果某个模块的路由没有被这里 `include_router` 进去，那它大概率还没正式接入对外接口。

### 方法二: 看 `app/models/__init__.py`

如果某个模型没有被这里导出，它大概率还没进入当前正式模型集合。

### 方法三: 看 `app/db/base.py`

如果某个模型没有被这里导入，Alembic 很可能也没把它当成当前正式迁移对象。

### 方法四: 看 `alembic/versions/`

如果 migration 里根本没有这张表，那它至少还没成为已经正式落库的稳定表结构。

### 方法五: 看有没有成套文件

一个真正已经成型的业务模块，通常至少会成套出现:

1. model
2. schema
3. service
4. route
5. router 接入
6. Alembic 接入

如果只出现了一两个文件，通常说明它还只是草稿。

---

## 10. 你现在最应该怎么用这份文档

最推荐的用法不是“把所有文件都平均地读一遍”，而是这样:

### 第一步

先只看“正式主链路”文件。

### 第二步

等你把:

1. 启动
2. 配置
3. 鉴权
4. 用户
5. Profile

这一整套读顺了，再回来看:

1. Record
2. Conversation
3. Proactive

### 第三步

每次看到一个陌生文件，先问自己两个问题:

1. 它有没有被总路由挂进去?
2. 它有没有被正式模型入口和 Alembic 入口接进去?

这两个问题一问，很多“文件明明在，但为什么没生效”的困惑就会立刻消失。

---

## 11. 一句话总结当前状态

按“第二阶段已经完成”的视角，你当前最应该把这些文件当作正式后端:

`main + core + db/session + deps + auth/users/profiles routes + auth/user/profile services + user/profile models + 对应 schemas + Alembic users/profiles migration`

而 `record / conversation / message / proactive / repository` 这些文件，当前更适合被理解成:

“后续阶段已经开始准备，但尚未完全并入当前稳定主链路的草稿或预留结构”
