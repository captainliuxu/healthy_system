# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
import dashscope
import sqlite3

sys.stdout.reconfigure(encoding='utf-8')

# ======================
# 基础配置
# ======================
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

app = FastAPI()

# CORS（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ======================
# 密码加密
# ======================
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ======================
# 数据库初始化（自动建库）
# ======================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT NOT NULL,
                  email TEXT,
                  phone TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ======================
# 请求体格式（和前端对应）
# ======================
class UserRegister(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str = ""
    phone: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

from fastapi.responses import JSONResponse

@app.post("/api/v1/auth/register")
def register(user: UserRegister):
    if user.password != user.confirm_password:
        return JSONResponse(status_code=400, content={"code": 1, "message": "两次密码不一致"})

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username=?", (user.username,))
    exists = c.fetchone()

    if exists:
        conn.close()
        return JSONResponse(status_code=400, content={"code": 1, "message": "用户名已存在"})

    hashed_pw = get_password_hash(user.password)
    c.execute(
        "INSERT INTO users (username, password, email, phone) VALUES (?, ?, ?, ?)",
        (user.username, hashed_pw, user.email, user.phone)
    )
    conn.commit()
    conn.close()

    return {"code": 0, "message": "注册成功"}

@app.post("/api/v1/auth/login")
def login(user: UserLogin):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, password FROM users WHERE username=?", (user.username,))
    record = c.fetchone()
    conn.close()

    if not record:
        raise HTTPException(status_code=400, detail="用户不存在")

    username, hashed_pw = record
    if not verify_password(user.password, hashed_pw):
        raise HTTPException(status_code=400, detail="密码错误")

    return {"code": 0, "message": "登录成功"}

# ======================
# 原来的聊天接口（不动）
# ======================
@app.get("/chat")
def chat(msg: str):
    if not dashscope.api_key:
        return {"reply": "后端未读取到 DASHSCOPE_API_KEY，请检查根目录 .env"}
    try:
        response = dashscope.Generation.call(
            model="qwen-turbo",
            messages=[{"role": "system", "content": "你是慢病健康管理助手"},
                      {"role": "user", "content": msg}]
        )
        return {"reply": response["output"]["text"]}
    except Exception as e:
        return {"reply": f"出错：{str(e)}"}