from pydantic import BaseModel, Field
from typing import Optional

# --- LLM Schemas ---

class LLMValidateRequest(BaseModel):
    api_key: str = Field(..., description="硅基流动 API Key")

class GenerateRequest(BaseModel):
    api_key: str
    topic: str
    article_type: str
    prompt_template: str

class RegenerateBlockRequest(BaseModel):
    api_key: str
    block_type: str # e.g., "CODE", "PLANTUML"
    description: str
    language: Optional[str] = None # For code blocks

# --- Prompt Schemas ---

class PromptBase(BaseModel):
    title: str

class PromptCreate(PromptBase):
    content: str

class Prompt(PromptBase):
    id: int
    content: str

    class Config:
        from_attributes = True


# --- Export Schemas ---
class ExportRequest(BaseModel):
    markdown_content: str
    export_format: str # 'pdf', 'docx', 'md'
