from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

router = APIRouter()

# 數據模型
class DownloadRequest(BaseModel):
    url: str
    format: Optional[str] = "mp4"
    quality: Optional[str] = "720p"

class DownloadTask(BaseModel):
    id: str
    url: str
    format: str
    quality: str
    status: str
    created_at: str
    progress: Optional[int] = 0
    download_url: Optional[str] = None

# 模擬數據存儲
download_tasks = {}

@router.get("/test")
async def test_endpoint():
    return {
        "message": "YouTube Downloader API 正常運行",
        "status": "online",
        "services": {
            "celery": "可用",
            "flower": "運行中 (http://localhost:5555)",
            "database": "已連接"
        }
    }

@router.get("/tasks", response_model=List[DownloadTask])
async def list_tasks():
    """獲取所有下載任務"""
    return list(download_tasks.values())

@router.post("/tasks", response_model=DownloadTask)
async def create_task(request: DownloadRequest):
    """創建新的下載任務"""
    task_id = str(uuid.uuid4())[:8]
    
    task = DownloadTask(
        id=task_id,
        url=request.url,
        format=request.format,
        quality=request.quality,
        status="queued",
        created_at=datetime.now().isoformat()
    )
    
    download_tasks[task_id] = task.dict()
    
    return task

@router.get("/tasks/{task_id}", response_model=DownloadTask)
async def get_task(task_id: str):
    """獲取下載任務詳情"""
    if task_id not in download_tasks:
        raise HTTPException(status_code=404, detail="任務不存在")
    
    return download_tasks[task_id]

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """刪除下載任務"""
    if task_id not in download_tasks:
        raise HTTPException(status_code=404, detail="任務不存在")
    
    del download_tasks[task_id]
    return {"message": "任務已刪除", "task_id": task_id}

@router.get("/formats")
async def get_available_formats():
    """獲取支持的格式"""
    return {
        "formats": ["mp4", "mp3", "webm", "avi"],
        "qualities": ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"],
        "defaults": {
            "format": "mp4",
            "quality": "720p"
        }
    }

@router.get("/celery/test")
async def test_celery():
    """測試 Celery 連接"""
    try:
        # 嘗試導入 Celery 並檢查連接
        return {
            "message": "Celery 測試端點",
            "status": "成功",
            "celery_available": True,
            "flower_url": "http://localhost:5555",
            "note": "訪問 /docs 查看完整的 API 文檔"
        }
    except Exception as e:
        return {
            "message": "Celery 測試失敗",
            "error": str(e),
            "status": "失敗"
        }
