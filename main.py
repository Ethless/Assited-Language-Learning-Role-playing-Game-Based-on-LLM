from fastapi import FastAPI
from api import item_api, npc_api, story_api, vocab_api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DeepSeek 对话服务")

app.include_router(item_api.router, prefix="/item", tags=["Item Chat"])
app.include_router(npc_api.router, prefix="/npc", tags=["NPC Chat"])
app.include_router(story_api.router, tags=["Story Generator"])
app.include_router(vocab_api.router, prefix="/api", tags=["Vocab Save"])

# 跨域CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者限定为 ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
