from fastapi import APIRouter
router = APIRouter(tags=["health"])


"""检查后端是否成功启动"""
@router.get("/health")
async def get_health():
    return {
        "status": "ok",
        "app": "Course Rag System"
    }