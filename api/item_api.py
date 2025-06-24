from fastapi import APIRouter
from pydantic import BaseModel
from core.DSchat import DeepSeekClient
from core.chatRobot import item_chat

router = APIRouter()
client = DeepSeekClient()
item_bot = item_chat(client)

class ItemSet(BaseModel):
    item_name: str
    item_description: str

class ItemInteract(BaseModel):
    option: str

@router.post("/set_item")
def set_item(info: ItemSet):
    item_bot.set_item(info.item_name, info.item_description)
    return {"message": "物品设置完成"}

@router.get("/options")
def get_options():
    return {"options": item_bot.generate_options()}

@router.post("/interact")
def interact_with_item(data: ItemInteract):
    return item_bot.interact(data.option)

@router.get("/memory")
def get_memory():
    return item_bot.get_all_memory()
