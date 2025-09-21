from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....db import crud, models, session
from ..schemas import PromptCreate, Prompt as PromptSchema

router = APIRouter()

@router.post("/prompts/", response_model=PromptSchema)
def create_prompt(prompt: PromptCreate, db: Session = Depends(session.get_db)):
    """
    创建一个新的提示词模板。
    """
    db_prompt = crud.get_prompt_by_title(db, title=prompt.title)
    if db_prompt:
        raise HTTPException(status_code=400, detail="Prompt with this title already exists")
    return crud.create_prompt(db=db, prompt=prompt)

@router.get("/prompts/", response_model=List[PromptSchema])
def read_prompts(skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)):
    """
    获取所有提示词模板。
    """
    prompts = crud.get_prompts(db, skip=skip, limit=limit)
    # 如果数据库为空，创建默认模板
    if not prompts:
        default_prompts = [
            PromptCreate(title="通用博文", content="你是一名专业的博主，擅长撰写引人入胜、内容详实的博客文章。"),
            PromptCreate(title="技术教程", content="你是一位资深的技术专家和导师，能够将复杂的技术概念分解为简单易懂的步骤。"),
            PromptCreate(title="推文", content="你是一位社交媒体达人，精通撰写简短、有力、易于传播的推文。"),
        ]
        for p in default_prompts:
            crud.create_prompt(db=db, prompt=p)
        prompts = crud.get_prompts(db, skip=skip, limit=limit)
    return prompts
