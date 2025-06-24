from fastapi import APIRouter
from pydantic import BaseModel
from core.DSchat import DeepSeekClient
from core.chatRobot import story_NPC_chat

router = APIRouter()

# 创建 NPC 对话管理实例
client = DeepSeekClient()
npc = story_NPC_chat(client)

# 请求体模型
class NPCSetting(BaseModel):
    name: str
    personality: str
    background: str
    environment: str = "未知地点"

class UserInput(BaseModel):
    user_input: str

@router.post("/set_npc")
def set_npc(setting: NPCSetting):
    npc.set_npc_setting(
        name=setting.name,
        personality=setting.personality,
        background=setting.background,
        environment=setting.environment
    )
    return {"message": f"NPC {setting.name} 设置完成"}

@router.get("/dialogue")
def get_dialogue():
    return npc.generate_dialogue()

@router.get("/options")
def get_options():
    return {"options": npc.generate_options()}

@router.post("/respond")
def respond(input: UserInput):
    npc.add_user_response(input.user_input)
    return {"message": "回应已记录"}

@router.get("/summary")
def get_summary():
    return npc.summarize_conversation()

@router.get("/goodbye")
def goodbye(reason: str = "有急事"):
    return npc.generate_goodbye(reason)

@router.get("/memory")
def get_memory():
    return {"memory": npc.get_all_memory()}
