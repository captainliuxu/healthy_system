# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dashscope

sys.stdout.reconfigure(encoding='utf-8')

# 显式读取项目根目录 .env
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
def chat(msg: str):
    if not dashscope.api_key:
        return {"reply": "后端未读取到 DASHSCOPE_API_KEY，请检查根目录 .env"}

    try:
        response = dashscope.Generation.call(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": "你是一个慢病健康管理助手，回答简洁、温和"},
                {"role": "user", "content": msg}
            ]
        )

        reply = response["output"]["text"]
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"调用失败：{str(e)}"}