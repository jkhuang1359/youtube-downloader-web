from .celery import celery_app

@celery_app.task(bind=True)
def test_task(self):
    """測試 Celery 是否正常工作的任務"""
    print("✅ Celery 任務執行成功！")
    return {"status": "success", "message": "Celery is working!"}

@celery_app.task(bind=True)
def download_youtube_video(self, url, format="mp4"):
    """下載 YouTube 影片的任務（範例）"""
    try:
        # 這裡會放實際的下載邏輯
        # 現在先返回一個模擬結果
        print(f"開始下載: {url}, 格式: {format}")
        
        # 模擬處理時間
        import time
        time.sleep(2)
        
        return {
            "status": "success",
            "url": url,
            "format": format,
            "filename": f"video_{int(time.time())}.{format}",
            "task_id": self.request.id
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@celery_app.task(bind=True)
def convert_video_format(self, input_file, output_format):
    """轉換影片格式的任務（範例）"""
    print(f"轉換 {input_file} 到 {output_format} 格式")
    return {
        "status": "success",
        "input": input_file,
        "output_format": output_format,
        "output_file": input_file.replace(".mp4", f".{output_format}")
    }
