from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api import item_api, npc_api, story_api, vocab_api, cloze_api
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI(title="DeepSeek 对话服务")

# 挂载你的业务路由
app.include_router(item_api.router, prefix="/item", tags=["Item Chat"])
app.include_router(npc_api.router, prefix="/npc", tags=["NPC Chat"])
app.include_router(story_api.router, tags=["Story Generator"])
app.include_router(vocab_api.router, prefix="/api", tags=["Vocab Save"])
app.include_router(cloze_api.router, tags=["Cloze Generator"])

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 新增：清空接口
@app.post("/clear_vocabulary")
async def clear_vocabulary():
    vocab_path = "./public/note/vocabulary.json"
    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False)
    return JSONResponse(content={"message": "Vocabulary cleared."})
