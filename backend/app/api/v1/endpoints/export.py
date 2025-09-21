from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
import os

from ..schemas import ExportRequest
from ....services.pandoc_service import PandocService, ConversionError

router = APIRouter()
pandoc_service = PandocService()

@router.post("/export")
async def export_document(request: ExportRequest):
    """
    将 Markdown 内容导出为指定格式 (pdf, docx, md)。
    """
    try:
        output_path, media_type = pandoc_service.convert(request.markdown_content, request.export_format)
        
        if request.export_format == 'md':
             return Response(content=request.markdown_content, media_type="text/markdown", headers={
                'Content-Disposition': f'attachment; filename="export.md"'
            })

        return FileResponse(
            path=output_path,
            media_type=media_type,
            filename=f"export.{request.export_format}",
            background=pandoc_service.create_cleanup_task(output_path)
        )
    except ConversionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
