import asyncio
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ....core.llm_service import SiliconFlowService, get_llm_service
from ..schemas import LLMValidateRequest, GenerateRequest, RegenerateBlockRequest
from ....db import crud, session as db_session
from ....db.models import Prompt

router = APIRouter()

@router.post("/llm/validate")
async def validate_api_key(
    request: LLMValidateRequest,
    llm_service: SiliconFlowService = Depends(get_llm_service)
):
    """
    校验用户提供的 API Key 是否有效。
    """
    is_valid, message = await llm_service.validate_key(request.api_key)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    return {"message": "API Key is valid."}

@router.post("/llm/generate")
async def generate_article(
    request: GenerateRequest,
    db: Session = Depends(db_session.get_db),
    llm_service: SiliconFlowService = Depends(get_llm_service)
):
    """
    根据主题和提示词模板流式生成文章。
    """
    prompt_template_obj: Prompt | None = crud.get_prompt_by_title(db, title=request.prompt_template)
    if not prompt_template_obj:
        raise HTTPException(status_code=404, detail="Prompt template not found")

    prompt = llm_service.construct_prompt(prompt_template_obj.content, request.article_type, request.topic)

    try:
        return StreamingResponse(
            llm_service.stream_generation(request.api_key, prompt),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/llm/regenerate-block")
async def regenerate_block(
    request: RegenerateBlockRequest,
    llm_service: SiliconFlowService = Depends(get_llm_service)
):
    """
    为特定的智能块（如代码、图表）重新生成内容。
    """
    prompt = llm_service.construct_block_regeneration_prompt(
        block_type=request.block_type,
        description=request.description,
        language=getattr(request, 'language', None)
    )

    try:
        return StreamingResponse(
            llm_service.stream_generation(request.api_key, prompt),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
