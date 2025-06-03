from fastapi import APIRouter
from pydantic import BaseModel
from core.DSchat import DeepSeekClient
from core.chatRobot import story_NPC_chat

router = APIRouter()
client = DeepSeekClient()
npc_bot = story_NPC_chat(client)

class NPCSetting(BaseModel):
    name: str
    personality: str
    background: str
    environment: str = "未知地点"

class UserInput(BaseModel):
    user_input: str

@router.post("/set_npc")
def set_npc(setting: NPCSetting):
    npc_bot.set_npc_setting(
        name=setting.name,
        personality=setting.personality,
        background=setting.background,
        environment=setting.environment
    )
    return {"message": "NPC设定成功"}

@router.get("/dialogue")
def generate_npc_dialogue():
    return npc_bot.generate_dialogue()

@router.get("/options")
def generate_npc_options():
    return {"options": npc_bot.generate_options()}

@router.post("/respond")
def respond_to_npc(input: UserInput):
    npc_bot.add_user_response(input.user_input)
    return {"message": "已记录用户输入"}

@router.get("/goodbye")
def goodbye(reason: str = "有急事"):
    return npc_bot.generate_goodbye(reason)

@router.get("/summary")
def get_summary():
    return npc_bot.summarize_conversation()

@router.get("/memory")
def get_npc_memory():
    return npc_bot.get_all_memory()
