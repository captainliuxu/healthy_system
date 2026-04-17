# 比赛项目后端开发顺序详细文档

## 文档目标

这份文档用于指导你当前比赛项目的后端开发顺序，目标不是一开始就把所有“高级功能”全部堆上去，而是按照**可运行、可验证、可扩展**的方式，一步一步把项目真正做起来。

你的项目里可能包含这些方向：

- 用户系统
- 健康档案 / Profile
- 健康记录 / Record
- 会话与消息 / Conversation & Message
- 聊天链路
- 主动提醒 / 主动服务
- 触发规则
- WebSocket 实时推送
- Scheduler 定时任务

这些模块之间是有依赖关系的，所以开发顺序很重要。

---

# 一、总原则

## 1. 先做“地基”，再做“功能”，最后做“增强体验”

推荐你始终遵守这条思路：

> **基础设施 → 核心 CRUD → 聊天闭环 → 主动能力 → 实时化 / 定时化**

原因很简单：

- 没有用户体系，后面的数据没法绑定到人
- 没有基础 CRUD，后面的智能能力没有数据来源
- 没有聊天闭环，主动服务就没有上下文基础
- 没有触发机制，WebSocket 和 scheduler 只是空壳

所以不要一开始就冲 WebSocket、定时任务、复杂 Agent，这样很容易把项目做散。

---

# 二、推荐总开发顺序

## 推荐顺序

1. 基础骨架层
2. 用户 / 认证 / Profile
3. Record 业务模块
4. Conversation / Message 模块
5. 聊天主链路落地
6. 主动日志与触发规则
7. 主动服务与主动窗口
8. WebSocket 与 Scheduler
9. 优化、测试、演示包装

---

# 三、阶段式开发方案

---

## 第一阶段：基础骨架层

### 阶段目标

先把项目跑起来，形成一个规范的后端基础工程，保证后面加功能不会乱。

### 这一阶段必须完成的内容

#### 1. 项目目录结构
建议至少拆成：

```text
app/
├─ api/
├─ core/
├─ models/
├─ schemas/
├─ services/
├─ db/
├─ utils/
└─ main.py
```

#### 2. 配置管理
包括：

- 开发环境配置
- 数据库连接配置
- JWT 配置
- 大模型 API Key 配置
- CORS 配置

建议统一放在：

- `app/core/config.py`

#### 3. 数据库连接与会话管理
包括：

- SQLAlchemy engine
- SessionLocal
- Base
- 数据库依赖注入

#### 4. 通用返回格式
统一接口返回结构，例如：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

#### 5. 全局异常处理
包括：

- 参数错误
- 业务错误
- 404
- 500

#### 6. Alembic 迁移初始化
你后面表会越来越多，不要靠手改数据库。

### 这一阶段不要做的事

- 不要碰聊天功能
- 不要碰 WebSocket
- 不要碰 scheduler
- 不要写很多业务逻辑

### 阶段验收标准

做到下面这些，就算第一阶段合格：

- 项目能启动
- `/docs` 可访问
- 数据库能连通
- 有统一响应格式
- 可以做 migration

---

## 第二阶段：用户 / 认证 / Profile

### 阶段目标

把“谁在使用系统”这件事先确定下来。

因为几乎所有业务表，最后都要挂到用户下面。

### 推荐顺序

1. User
2. Auth
3. Profile

---

### 2.1 User 模块

#### 建议先做的字段

```text
id
username
email
phone
password_hash
is_active
created_at
updated_at
```

#### 建议接口

- 用户注册
- 用户登录
- 获取当前用户信息
- 修改基本信息

---

### 2.2 Auth 模块

#### 建议内容

- 密码加密
- JWT 登录
- 当前用户依赖注入
- 路由鉴权

#### 最低要求

至少实现：

- 注册
- 登录
- 受保护接口访问

---

### 2.3 Profile 模块

Profile 建议理解成“用户健康档案 / 用户画像”，而不是登录账号本身。

#### 建议字段

根据你的比赛项目可以先简化，例如：

```text
id
user_id
name
age
gender
height
weight
chronic_history
allergy_history
emergency_contact
remark
```

#### 建议接口

- 创建 profile
- 查看 profile
- 更新 profile

### 为什么先做 Profile

因为后面的：

- 健康记录
- 聊天建议
- 主动提醒
- 个性化推荐

通常都需要 profile 作为基础上下文。

### 阶段验收标准

- 用户可注册登录
- 用户身份可鉴权
- 每个用户能维护自己的 profile

---

## 第三阶段：Record 模块

### 阶段目标

先完成一个完整、清晰、好演示的业务 CRUD 模块。

Record 适合先做，因为它相对独立，最适合练完整开发流程。

### Record 是什么

Record 可以是：

- 健康打卡记录
- 血压记录
- 血糖记录
- 睡眠记录
- 用药记录
- 心情记录

你比赛里不需要一开始就做得特别复杂，先统一成一个基础记录表即可。

### 推荐最小模型

```text
id
user_id
record_type
value
unit
record_time
note
created_at
updated_at
```

或者你也可以先拆几个通用字段：

```text
id
user_id
category
content
measure_value
measure_unit
record_time
remark
```

### 建议接口

- 创建记录
- 获取记录列表
- 获取记录详情
- 更新记录
- 删除记录

### 推荐额外补的能力

- 分页
- 按类型筛选
- 按时间筛选

### 这一阶段的重要意义

它会帮你真正练到：

- model
- schema
- router
- service
- CRUD
- 数据验证
- 查询过滤

这是后面所有模块的模板。

### 阶段验收标准

- 记录模块 CRUD 完整
- 每条记录归属当前用户
- 支持基础筛选
- Swagger 可直接演示

---

## 第四阶段：Conversation / Message 模块

### 阶段目标

先把聊天数据结构建好，但这时候先不要急着接大模型。

### 为什么先做数据结构

因为聊天功能本质上至少有两层：

1. 会话（conversation）
2. 消息（message）

如果数据模型不先稳定，后面接模型调用时你会不断返工。

---

### 4.1 Conversation 模块

#### 建议字段

```text
id
user_id
title
status
created_at
updated_at
```

#### 建议接口

- 创建会话
- 获取会话列表
- 获取会话详情
- 修改会话标题
- 删除会话

---

### 4.2 Message 模块

#### 建议字段

```text
id
conversation_id
role
content
message_type
created_at
```

#### role 建议值

- user
- assistant
- system

#### 建议接口

- 获取某会话消息列表
- 手动插入消息（调试用）

### 这一阶段先不要做的事

- 不要急着流式输出
- 不要急着 WebSocket
- 不要急着复杂 prompt 编排

### 先验目标

你只要做到：

- 用户能创建会话
- 用户能查历史消息
- 消息能落库

就已经完成这一阶段的目标。

### 阶段验收标准

- conversation 与 user 正确关联
- message 与 conversation 正确关联
- 历史消息可查询

---

## 第五阶段：聊天主链路落地

### 阶段目标

真正打通一条最小可用聊天链路：

> 用户发消息 → 写入 user message → 调用大模型 / 规则引擎 → 生成 assistant message → 回复前端

这一步是整个项目从“静态管理系统”变成“智能应用”的关键。

---

### 推荐先实现的最小版本

#### 输入

前端发来：

- conversation_id
- 用户消息内容

#### 后端流程

1. 校验 conversation 是否属于当前用户
2. 保存 user message
3. 读取最近若干条历史消息
4. 拼 prompt 或构造 messages
5. 调用模型
6. 保存 assistant message
7. 返回结果

---

### 推荐封装

建议把模型调用单独封装在：

- `app/services/chat_service.py`
- `app/services/llm_service.py`

不要直接把调用模型的代码塞到 router 里。

---

### 这一阶段建议先做同步版本

也就是先普通 HTTP 请求返回，不要一开始就搞流式。

原因：

- 好调试
- 好定位报错
- 便于先验证数据库链路
- 逻辑更容易看懂

### 这一阶段推荐接口

- `POST /chat/send`
- `GET /conversations/{id}/messages`

### 阶段验收标准

- 发一条消息能拿到 AI 回复
- 用户消息和 AI 回复都能入库
- 历史消息能回显

---

## 第六阶段：主动日志与触发规则

### 阶段目标

开始为“主动服务”打地基。

很多项目喜欢一上来就说“主动关怀”“智能提醒”，但如果没有触发规则和日志，这些功能都很空。

所以这阶段先做两个底层模块：

1. trigger rule（触发规则）
2. active log（主动行为日志）

---

### 6.1 Trigger Rule

#### 它是干什么的

定义系统在什么情况下要主动介入。

例如：

- 用户 3 天没记录健康数据
- 用户血压超阈值
- 用户情绪连续低落
- 用户最近聊天表达焦虑倾向

#### 最小字段建议

```text
id
name
trigger_type
enabled
condition_json
priority
created_at
updated_at
```

#### condition_json 可以存什么

例如：

```json
{
  "days_without_record": 3,
  "record_type": "blood_pressure"
}
```

---

### 6.2 Active Log

#### 它是干什么的

记录系统每一次主动行为：

- 为什么触发
- 对谁触发
- 触发时机
- 做了什么动作
- 成功还是失败

#### 最小字段建议

```text
id
user_id
trigger_rule_id
action_type
status
request_payload
response_payload
created_at
```

### 为什么先做日志再做主动服务

因为只做“主动发送”不做日志，后期你根本查不清：

- 为什么触发了
- 触发错了没有
- 是不是重复触发
- 哪些规则效果最好

### 阶段验收标准

- 规则可配置
- 可手动触发规则检查
- 日志可记录一次触发过程
- `trigger_rule` 能存配置条件
- `active_log` 能记录一次检查结果
- 用户只能查看自己的主动日志

---

## 第七阶段：主动服务与主动窗口

### 阶段目标

让系统开始具备“主动触达用户”的能力。

这一层才是比赛里比较亮眼的部分，但它必须建立在前面的数据和日志基础之上。

---

### 7.1 主动服务

#### 可以理解成什么

根据触发规则，系统决定向用户执行某种动作，例如：

- 推送提醒
- 生成建议消息
- 弹出健康关怀提示
- 写入一条主动 assistant message

#### 推荐最小版本

不要一开始就做真实通知推送，先做：

- 在 conversation 里插入一条系统主动消息
- 或者在主动消息表中生成待展示内容

这样更容易演示，也更容易测试。

---

### 7.2 主动窗口

主动窗口可以理解为：

> 在什么时间段 / 什么场景下允许主动打扰用户

例如：

- 只在 8:00 - 22:00 之间主动触发
- 同一用户 24 小时内最多主动一次
- 某类事件优先级更高

#### 建议先不用做很复杂

可以先做简单字段：

```text
quiet_hours_start
quiet_hours_end
max_trigger_per_day
```

或者直接放在配置表 / 用户偏好表中。

### 阶段验收标准

- 系统可根据规则生成主动消息
- 能限制主动频率
- 能记录主动行为日志

---

## 第八阶段：WebSocket 与 Scheduler

### 阶段目标

把系统从“能用”升级到“更像真实产品”。

这两个都属于增强层，而不是最前置层。

---

### 8.1 WebSocket

#### 适合放在后面的原因

因为它解决的是：

- 实时推送
- 流式返回
- 即时刷新

但它不决定你的核心业务逻辑是否成立。

如果你前面聊天主链路都没打通，直接做 WebSocket 只会让调试更复杂。

#### 推荐使用场景

- 聊天流式输出
- 主动提醒实时弹出
- 在线状态同步

#### 推荐先做什么

先做最小版：

- 建立连接
- 向当前用户推一条文本消息

不要一开始就写复杂的房间管理。

---

### 8.2 Scheduler

#### 它是干什么的

定期执行规则扫描、提醒任务、归档任务等。

例如：

- 每天早上 8 点检查未打卡用户
- 每小时扫描高风险记录
- 每天总结用户健康数据

#### 推荐技术

FastAPI 项目里你可以后续考虑：

- APScheduler
- Celery（更重，暂时不推荐第一版就上）

#### 为什么最后做

因为 scheduler 依赖：

- 规则已经定义好
- 主动服务已经可执行
- 日志系统已经存在

否则它只是“定时空转”。

### 阶段验收标准

- 能定时执行触发检查
- 触发后能记录日志
- 可以选配 WebSocket 推送到前端

---

## 第九阶段：测试、优化、演示包装

### 阶段目标

为比赛做最终展示准备。

这一阶段不是继续疯狂加功能，而是让已有功能稳定、清晰、可演示。

### 重点内容

#### 1. 接口测试

建议至少测：

- 注册 / 登录
- Profile CRUD
- Record CRUD
- Conversation / Message 查询
- Chat send
- Trigger check

#### 2. 权限测试

重点看：

- 用户 A 是否能访问用户 B 的数据
- conversation 是否能越权访问
- record 是否能越权修改

#### 3. 演示数据准备

比赛项目一定要准备演示账号与演示数据。

#### 4. Swagger 文档整理

- tags 分组清晰
- 示例请求清晰
- 响应模型清晰

#### 5. README 补全

至少写清楚：

- 项目简介
- 技术栈
- 目录结构
- 启动方式
- 主要模块

---

# 四、每个阶段的依赖关系

可以用下面这个逻辑记：

```text
基础骨架
  ↓
User / Auth / Profile
  ↓
Record
  ↓
Conversation / Message
  ↓
Chat 主链路
  ↓
Trigger Rule / Active Log
  ↓
Active Service / Active Window
  ↓
WebSocket / Scheduler
```

---

# 五、你原始顺序的评价

你原来的思路是：

1. 先把 profile 做好
2. 再把 record 做好
3. 再补 conversation 和 message
4. 再让聊天链路落地
5. 再做主动窗口和主动日志
6. 再做触发服务和主动服务
7. 最后才做 WebSocket 和 scheduler

## 结论

这个思路整体是对的，已经比“先做高级功能”强很多。

但是建议你补一个更前置的阶段：

> **Profile 前面还要先有 User / Auth / 基础设施**

否则后面很多表会因为缺 user_id、权限体系、登录状态而返工。

另外还有一个建议：

> **主动日志最好放在主动窗口前面，作为更底层的追踪能力。**

所以更合理的版本是：

1. 基础骨架
2. User / Auth
3. Profile
4. Record
5. Conversation / Message
6. Chat 主链路
7. Trigger Rule / Active Log
8. Active Service / Active Window
9. WebSocket / Scheduler

---

# 六、最适合你当前比赛项目的执行版顺序

下面给你一个更接地气的“真正照着做”的版本。

## 第 1 批

- 项目结构
- config
- database
- BaseModel
- 通用响应
- 异常处理
- Alembic

## 第 2 批

- user model
- register/login
- JWT 鉴权
- current user 依赖
- profile model + CRUD

## 第 3 批

- record model
- record CRUD
- record 筛选查询

## 第 4 批

- conversation model
- message model
- conversation CRUD
- message list 查询

## 第 5 批

- chat/send 接口
- 用户消息入库
- 调用模型
- assistant 回复入库

## 第 6 批

- trigger rule model
- active log model
- 规则检查 service

## 第 7 批

- 主动消息 service
- 主动窗口限制
- 频率控制

## 第 8 批

- scheduler 定时检查
- websocket 主动推送
- 聊天流式输出（可选）

## 第 9 批

- 测试
- 优化
- 演示脚本
- README

---

# 七、每个阶段“不要做什么”总结

## 第一阶段不要做

- 不要接模型
- 不要写业务细节
- 不要搞 WebSocket

## 第二阶段不要做

- 不要把 profile 和 user 混成一个表后又反复改
- 不要跳过 auth

## 第三阶段不要做

- 不要过度设计 record 类型
- 不要一开始拆十几张记录表

## 第四阶段不要做

- 不要一开始就做复杂多轮记忆
- 不要先上流式输出

## 第五阶段不要做

- 不要把模型调用逻辑写死在 router
- 不要不落库直接返回

## 第六七阶段不要做

- 不要只做“主动提醒”界面，不做触发规则与日志
- 不要没有频率控制就主动触发

## 第八阶段不要做

- 不要在核心链路没稳时硬上 WebSocket
- 不要一开始就上 Celery 全家桶

---

# 八、最终一句话版

你最应该遵循的开发顺序是：

> **基础设施 → 用户认证与 Profile → Record → Conversation / Message → 聊天主链路 → 触发规则与主动日志 → 主动服务 → WebSocket / Scheduler**

这是最适合你当前比赛项目的后端开发顺序。

---

# 九、下一步建议

你现在最适合继续做的是：

1. 按这个顺序建立项目目录
2. 先完成 User / Auth / Profile
3. 再开始写 Record 的完整 CRUD

如果你愿意，下一份我可以继续给你写：

- **第一阶段详细文件开发清单.md**
- 或者 **FastAPI 比赛项目后端目录结构模板.md**
