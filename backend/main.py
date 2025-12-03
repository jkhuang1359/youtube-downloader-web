from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="YouTube Downloader API",
    description="一個簡單的 YouTube 視頻下載器 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境中應該設置具體的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 導入路由
from api.endpoints import download as download_endpoints
app.include_router(
    download_endpoints.router,
    prefix="/api/download",
    tags=["download"]
)

# 創建下載目錄（如果不存在）
os.makedirs("downloads", exist_ok=True)

# 靜態文件服務（用於提供下載的文件）
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

@app.get("/")
async def root():
    return {
        "message": "歡迎使用 YouTube Downloader API",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "download_api": "/api/download",
            "download_docs": "/docs#/download"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "youtube-downloader-api"}

@app.get("/info")
async def api_info():
    return {
        "name": "YouTube Downloader API",
        "version": "1.0.0",
        "description": "一個簡單的 YouTube 視頻下載器 API",
        "author": "Your Name",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "API 根路徑"},
            {"path": "/health", "method": "GET", "description": "健康檢查"},
            {"path": "/api/download/tasks", "method": "GET", "description": "獲取所有下載任務"},
            {"path": "/api/download/tasks", "method": "POST", "description": "創建下載任務"},
            {"path": "/api/download/tasks/{task_id}", "method": "GET", "description": "獲取任務詳情"},
            {"path": "/api/download/tasks/{task_id}", "method": "DELETE", "description": "刪除任務"},
            {"path": "/api/download/formats", "method": "GET", "description": "獲取支持的格式"}
        ]
    }
