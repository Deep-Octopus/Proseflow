from sqlalchemy.orm import Session
from . import models
from ..api.v1 import schemas

def get_prompt(db: Session, prompt_id: int):
    return db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()

def get_prompt_by_title(db: Session, title: str):
    return db.query(models.Prompt).filter(models.Prompt.title == title).first()

def get_prompts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prompt).offset(skip).limit(limit).all()

def create_prompt(db: Session, prompt: schemas.PromptCreate):
    db_prompt = models.Prompt(title=prompt.title, content=prompt.content)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt
