# vue_fastapi

一个基于 `Vue 3 + FastAPI + SQLAlchemy + Alembic` 的健康陪伴系统。当前代码已完成前八个阶段，并在第九阶段补齐了测试、README、演示数据脚本和北京时间统一处理。

## 当前阶段

- 已完成后端核心模块：用户认证、Profile、Record、Conversation/Message、Chat、Trigger Rule、Active Log、Proactive、WebSocket、Scheduler
- 已完成第九阶段交付：
  - 后端接口自动化测试
  - 北京时间统一修复
  - 演示数据脚本
  - Swagger 分组整理
  - README 与验收文档

## 技术栈

- 前端：Vue 3、Vite
- 后端：FastAPI、SQLAlchemy 2.x、Pydantic 2.x
- 数据库：SQLite
- 迁移：Alembic
- 定时任务：APScheduler

## 目录结构

```text
backend/
├─ alembic/                # 数据库迁移
├─ app/
│  ├─ api/                 # 路由与依赖
│  ├─ core/                # 配置、异常、响应、时区、调度
│  ├─ db/                  # 数据库会话与 Base
│  ├─ models/              # SQLAlchemy 模型
│  ├─ schemas/             # Pydantic 模型
│  ├─ services/            # 业务服务
│  └─ ws/                  # WebSocket 管理
├─ scripts/                # 演示脚本
└─ tests/                  # 第九阶段接口测试

frontend/
└─ src/
```

## 后端启动

进入后端目录：

```bash
cd backend
```

安装依赖：

```bash
pip install -r requirements.txt
```

执行迁移：

```bash
alembic upgrade head
```

启动后端：

```bash
uvicorn app.main:app --reload
```

启动后访问：

- Swagger：`http://127.0.0.1:8000/docs`
- OpenAPI：`http://127.0.0.1:8000/openapi.json`

## 前端启动

进入前端目录：

```bash
cd frontend
npm install
npm run dev
```

默认访问：

- 前端：`http://127.0.0.1:5173`

## 第九阶段测试

在 `backend` 目录执行：

```bash
pytest tests -q
```

当前覆盖内容：

- 注册 / 登录
- Profile CRUD
- Record CRUD
- Conversation / Message
- Chat send
- Trigger check
- 越权访问校验
- 北京时间断言

## 演示数据

在 `backend` 目录执行：

```bash
python scripts/seed_demo_data.py
```

脚本会自动准备：

- 演示账号
- 演示 Profile
- 演示 Record
- 演示 Conversation / Message
- 演示 Trigger Rule
- 演示 Proactive Window

## 北京时间说明

当前所有核心业务时间统一按 `Asia/Shanghai` 处理，包括：

- `created_at`
- `updated_at`
- `record_time`
- `displayed_at`
- WebSocket 推送时间
- 触发检查 / 主动服务执行时间

如果你是从旧版本升级，请先执行：

```bash
alembic upgrade head
```

最新迁移会把旧库里按 UTC 墙上时间存储的历史数据整体转换成北京时间。

## 主要模块

- `auth`：注册、登录、JWT
- `users`：当前用户信息
- `profiles`：健康档案
- `records`：健康记录
- `conversations` / `messages`：会话与消息
- `chat`：聊天主链路
- `trigger-rules`：规则配置与检查
- `active-logs`：主动行为日志
- `proactive`：主动窗口与主动消息
- `realtime`：WebSocket 与测试推送

## 验收文档

详细验收步骤见：

- [backend/PHASE9_ACCEPTANCE.md](backend/PHASE9_ACCEPTANCE.md)
