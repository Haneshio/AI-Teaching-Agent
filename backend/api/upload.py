from fastapi  import APIRouter,UploadFile,File,Depends
from backend.services.upload_service import upload
from backend.db.database import get_database
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(tags=["upload"])

"""接收用户上传的文件,并上传"""
@router.post("/api/upload",summary="文件上传")
async def upload_file(
        file:UploadFile=File(...),
        db:AsyncSession=Depends(get_database)
):
    return await upload(file,db)




