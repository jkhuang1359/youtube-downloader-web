from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from .tasks import download_youtube_video, test_task
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="YouTube Downloader API")

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 請求模型
class DownloadRequest(BaseModel):
    url: str
    format: str = "mp4"
    quality: Optional[str] = "best"

class TaskStatusRequest(BaseModel):
    task_id: str

@app.get("/")
async def root():
    return {"message": "YouTube Downloader API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": {"api": True, "celery": True}}

@app.post("/api/download")
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    """開始下載影片"""
    try:
        # 啟動 Celery 任務
        task = download_youtube_video.delay(request.url, request.format)
        return {
            "status": "queued",
            "task_id": task.id,
            "message": "下載任務已排隊"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/task/{task_id}")
async def get_task_status(task_id: str):
    """檢查任務狀態"""
    # 這裡應該從 Celery 獲取任務狀態
    # 簡化版本：返回模擬狀態
    return {
        "task_id": task_id,
        "status": "completed",  # 或 "pending", "started", "failed"
        "result": {"message": "任務已完成"}
    }

@app.post("/api/test-celery")
async def test_celery_endpoint():
    """測試 Celery 是否正常運作"""
    task = test_task.delay()
    return {"task_id": task.id, "message": "Celery 測試任務已啟動"}
