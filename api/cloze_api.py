from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from core.DSchat import DeepSeekClient
from core.clozeGenerator import ClozeGenerator  # 你可以把 ClozeGenerator 放在 core 里

# 创建路由
router = APIRouter()

# 初始化大模型客户端和完形填空生成器
client = DeepSeekClient()
cloze_generator = ClozeGenerator(client)

# 请求体模型
class WordItem(BaseModel):
    jp: str
    zh: str

class ClozeRequest(BaseModel):
    background_story: str
    word_list: List[WordItem]
    count: int = 1  # 可选，默认为 1

@router.post("/cloze/generate")
def generate_cloze(data: ClozeRequest):
    """
    生成一个或多个完形填空题目
    """
    if data.count == 1:
        result = cloze_generator.generate_cloze(
            data.background_story,
            [word.dict() for word in data.word_list]
        )
        return result
    else:
        result = cloze_generator.generate_multiple_cloze(
            data.background_story,
            [word.dict() for word in data.word_list],
            count=data.count
        )
        return {"results": result}
