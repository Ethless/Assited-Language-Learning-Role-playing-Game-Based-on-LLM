from fastapi import APIRouter
from pydantic import BaseModel
from core.DSchat import DeepSeekClient
from core.storyteller import storyteller, PERSPECTIVE_FIRST_PERSON, PERSPECTIVE_THIRD_PERSON

router = APIRouter()

# 初始化客户端和故事生成器
client = DeepSeekClient()
story = storyteller(client)

# 请求体模型
class StorySetup(BaseModel):
    background: str
    ending: str
    scene: str

class ItemInput(BaseModel):
    item: str

class SummaryInput(BaseModel):
    summary: str

@router.post("/story/setup")
def setup_story(data: StorySetup):
    story.set_background(data.background)
    story.set_ending(data.ending)
    story.update_scene(data.scene)
    return {"message": "设定完成"}

@router.post("/story/add_item")
def add_item(data: ItemInput):
    story.add_collected_items([data.item])
    return {"message": "物品已添加"}

@router.post("/story/add_summary")
def add_summary(data: SummaryInput):
    story.add_plot_summary(data.summary)
    return {"message": "剧情摘要已添加"}

@router.get("/story/plot/first")
def first_person_plot():
    return story.generate_plot(PERSPECTIVE_FIRST_PERSON)

@router.get("/story/plot/third")
def third_person_plot():
    return story.generate_plot(PERSPECTIVE_THIRD_PERSON)

@router.get("/story/ending")
def ending_transition():
    return story.generate_ending_transition(PERSPECTIVE_THIRD_PERSON)
