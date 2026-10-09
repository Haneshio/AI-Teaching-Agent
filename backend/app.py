from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.chat import router as chat_router
from backend.api.health import router as health_router
from backend.api.upload import router as upload_router
from backend.db.database import get_database,create_tables
from contextlib import asynccontextmanager

"""启动时，创建数据库连接"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()   # 启动执行建表
    yield   #运行中停留在此处
    # 关闭时，执行后续的清理逻辑


app=FastAPI(
    title="AI Teaching System", #设置 API 文档的项目标题。
    lifespan=lifespan,  #设置应用启动和关闭时要执行的逻辑
)

# 允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(health_router)
app.include_router(upload_router)