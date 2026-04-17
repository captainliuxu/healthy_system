# 第九阶段验收教程

本文档用于验收以下内容：

- 第九阶段是否完成
- 北京时间修复是否生效
- 自动化测试是否通过
- 演示数据是否可直接用于 Swagger / 前端演示

## 1. 验收目标

本次验收重点确认 4 件事：

1. 后端核心接口能正常工作
2. 越权访问被正确拦截
3. 所有业务时间统一为北京时间 `Asia/Shanghai`
4. 第九阶段的测试、README、演示脚本已经补齐

## 2. 验收前准备

在项目根目录打开 PowerShell。

进入后端目录：

```powershell
cd D:\vue_fastapi\backend
```

如果你还没有执行过最新迁移，先执行：

```powershell
alembic upgrade head
```

这一步很重要。最新迁移会把旧版本里按 UTC 墙上时间落库的历史时间数据统一转换成北京时间。

## 3. 自动化验收

运行后端测试：

```powershell
D:\vue_fastapi\backend\.venv\Scripts\python.exe -m pytest D:\vue_fastapi\backend\tests -q
```

预期结果：

- 所有测试通过
- 重点覆盖：
  - 注册 / 登录
  - Profile CRUD
  - Record CRUD
  - Conversation / Message
  - Chat send
  - Trigger check
  - 越权访问
  - 北京时间断言

## 4. 准备演示数据

执行演示脚本：

```powershell
D:\vue_fastapi\backend\.venv\Scripts\python.exe D:\vue_fastapi\backend\scripts\seed_demo_data.py
```

默认会准备一个演示账号：

- 用户名：`demo_beijing`
- 密码：`Demo123456`

如果你不想用默认账号，可以在执行前设置环境变量：

```powershell
$env:DEMO_USERNAME="your_demo_user"
$env:DEMO_PASSWORD="YourDemo123456"
```

## 5. 启动后端

```powershell
cd D:\vue_fastapi\backend
D:\vue_fastapi\backend\.venv\Scripts\uvicorn.exe app.main:app --reload
```

打开 Swagger：

- `http://127.0.0.1:8000/docs`

## 6. 手工验收步骤

### 6.1 登录

在 Swagger 中打开 `auth -> POST /api/v1/auth/login`

填写：

- `username`: `demo_beijing`
- `password`: `Demo123456`

执行后拿到 `access_token`。

点击右上角 `Authorize`，填入：

```text
Bearer 你的 access_token
```

### 6.2 检查用户时间

打开 `users -> GET /api/v1/users/me`

预期：

- 返回成功
- `created_at`、`updated_at` 带 `+08:00`
- 示例格式应类似：

```text
2026-04-17T18:30:45.123456+08:00
```

如果你看到 `Z`、`+00:00`，或者时间明显慢 8 小时，说明北京时间修复没有生效。

### 6.3 检查 Profile

打开 `profiles -> GET /api/v1/profiles/me`

预期：

- 能读到演示档案
- `created_at`、`updated_at` 是北京时间

再执行 `profiles -> PUT /api/v1/profiles/me`

例如修改：

```json
{
  "weight": 65.5,
  "remark": "验收时修改"
}
```

预期：

- 更新成功
- `updated_at` 变为当前北京时间

### 6.4 检查 Record

打开 `records -> POST /api/v1/records`

示例请求：

```json
{
  "record_type": "blood_pressure",
  "value": "118/78",
  "unit": "mmHg",
  "note": "验收新增记录"
}
```

预期：

- 创建成功
- `record_time`、`created_at`、`updated_at` 都是北京时间

再执行：

- `GET /api/v1/records`
- `GET /api/v1/records/{record_id}`
- `PUT /api/v1/records/{record_id}`
- `DELETE /api/v1/records/{record_id}`

确认 CRUD 全链路正常。

### 6.5 检查 Conversation / Message

打开 `conversations -> POST /api/v1/conversations`

示例请求：

```json
{
  "title": "第九阶段验收会话"
}
```

预期：

- 会话创建成功
- `created_at`、`updated_at` 为北京时间

然后打开 `chat -> POST /api/v1/chat/send`

示例请求：

```json
{
  "conversation_id": 你的会话ID,
  "content": "我最近晚上有点睡不好，也会有点焦虑。"
}
```

预期：

- 能返回 AI 回复
- 返回里的 `replied_at` 是北京时间

最后打开 `messages -> GET /api/v1/conversations/{conversation_id}/messages`

预期：

- 至少能看到 2 条消息
- `created_at` 都是北京时间

### 6.6 检查 Trigger Rule / Active Log

先创建一条触发规则：

打开 `trigger-rules -> POST /api/v1/trigger-rules`

示例请求：

```json
{
  "name": "验收-焦虑关键词",
  "trigger_type": "recent_chat_keyword",
  "enabled": true,
  "condition_json": {
    "keywords": ["焦虑"],
    "recent_limit": 10
  },
  "priority": 10
}
```

然后执行：

- `POST /api/v1/trigger-rules/{rule_id}/check/me`

预期：

- 如果最近消息里包含“焦虑”，则 `triggered = true`
- 返回 `created_at` 为北京时间

再执行：

- `GET /api/v1/active-logs`

预期：

- 能看到刚才生成的日志
- `created_at` 为北京时间

## 7. 越权验收

这部分建议你自己再注册一个新账号做交叉验证。

验收方法：

1. 用账号 A 创建一条 Record 或 Conversation
2. 切换到账号 B
3. 直接访问账号 A 的 `record_id` 或 `conversation_id`

预期：

- 访问被拒绝
- 不应读到别人的数据

## 8. 北京时间验收标准

以下字段都应该表现为北京时间：

- `users.created_at`
- `users.updated_at`
- `profiles.created_at`
- `profiles.updated_at`
- `records.record_time`
- `records.created_at`
- `records.updated_at`
- `conversations.created_at`
- `conversations.updated_at`
- `messages.created_at`
- `trigger_rules.created_at`
- `trigger_rules.updated_at`
- `active_logs.created_at`
- `proactive_messages.created_at`
- `proactive_messages.displayed_at`
- WebSocket 推送里的 `connected_at` / `sent_at`

通过标准：

- 返回值带 `+08:00`
- 和你本地北京时间一致
- 不再出现明显慢 8 小时的问题

## 9. 常见问题排查

### 9.1 时间还是不对

先确认你已经执行：

```powershell
alembic upgrade head
```

如果没执行，旧数据还是会保留 UTC 墙上时间。

### 9.2 演示账号没生成

重新执行：

```powershell
D:\vue_fastapi\backend\.venv\Scripts\python.exe D:\vue_fastapi\backend\scripts\seed_demo_data.py
```

### 9.3 Chat send 调不通

确认 `.env` 里这些配置有效：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_NAME`

## 10. 验收结论标准

满足下面几条，即可认为第九阶段完成：

1. 自动化测试全部通过
2. Swagger 可完成核心链路手工验证
3. 越权访问被拦截
4. 演示数据脚本可复用
5. 所有核心时间字段均为北京时间
