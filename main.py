# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dashscope

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 填你的 key
dashscope.api_key = "sk-639637cb5bcf466682a306c1e0c66d4f"

@app.get("/chat")
def chat(msg: str):
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