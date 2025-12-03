from celery import shared_task
import time

@shared_task(bind=True, name="download_youtube_video")
def download_youtube_video(self, task_id: str, url: str, format: str = "mp4"):
    """下載 YouTube 影片任務"""
    try:
        print(f"[Celery] 開始下載: {url}")
        
        # 模擬下載過程
        for i in range(1, 11):
            time.sleep(1)
            self.update_state(
                state="PROGRESS",
                meta={
                    "current": i * 10,
                    "total": 100,
                    "status": f"下載中... {i * 10}%"
                }
            )
            print(f"[Celery] 進度: {i * 10}%")
        
        return {
            "status": "success",
            "task_id": task_id,
            "url": url,
            "format": format,
            "filename": f"video_{task_id[:8]}.{format}"
        }
    except Exception as e:
        return {
            "status": "error",
            "task_id": task_id,
            "error": str(e)
        }

@shared_task
def test_task():
    """測試任務"""
    return {"message": "Celery is working!", "status": "success"}
