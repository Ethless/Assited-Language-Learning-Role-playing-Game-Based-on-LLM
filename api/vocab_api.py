from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union
import json
import os

router = APIRouter()

SAVE_FILE = "public/note/vocabulary.json"
SELECTION_FILE = "src/assets/selection.json"  # 确保相对路径或绝对路径正确

class VocabItem(BaseModel):
    id: Union[int, str]
    correct_judge: Union[int, str]

@router.post("/save-vocab")
async def save_vocab(item: VocabItem):
    try:
        # 读取已有保存文件内容
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []

        # 检查 selection.json 文件是否存在
        if not os.path.exists(SELECTION_FILE):
            return {"message": "selection.json 文件不存在，无法查找词条"}

        # 读取 selection.json
        with open(SELECTION_FILE, "r", encoding="utf-8") as f:
            selection_data = json.load(f)

        # 根据 id 查找词条
        vocab_info = None
        for entry in selection_data:
            if entry.get("id") == item.id:
                vocab_info = {
                    "id": entry.get("id"),
                    "name": entry.get("name"),
                    "zh": entry.get("zh"),
                    "jp": entry.get("jp"),
                    "correct_num": entry.get("correct_num"),
                    "correct_judge": int(item.correct_judge)
                }
                break

        if not vocab_info:
            return {"message": f"在 selection.json 中未找到 id={item.id} 的词条"}

        # 如果已存在，则跳过，不保存
        for entry in data:
            if entry.get("id") == item.id:
                return {"message": f"id={item.id} 已存在，跳过保存", "skipped": True}

        # 否则添加新词条
        data.append(vocab_info)

        # 保存回文件
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {"message": "保存成功", "savedItem": vocab_info}
    except Exception as e:
        return {"message": "保存失败", "error": str(e)}
