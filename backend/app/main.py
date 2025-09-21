from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.session import engine
from .db import models
from .api.v1.endpoints import llm, prompts, export

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proseflow API",
    description="Proseflow 文章生成器的后端服务",
    version="1.0.0"
)

# 配置 CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 API 路由
app.include_router(llm.router, prefix="/api/v1", tags=["LLM"])
app.include_router(prompts.router, prefix="/api/v1", tags=["Prompts"])
app.include_router(export.router, prefix="/api/v1", tags=["Export"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Proseflow API!"}