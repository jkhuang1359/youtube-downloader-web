from celery_app import celery_app
import time
import random
from datetime import datetime

@celery_app.task(bind=True)
def download_video_task(self, url, format='mp4', quality='720p'):
    """下載視頻的 Celery 任務"""
    task_id = self.request.id
    
    # 模擬下載過程
    total_steps = 10
    for i in range(1, total_steps + 1):
        time.sleep(1)  # 模擬工作
        progress = int((i / total_steps) * 100)
        
        # 更新任務狀態
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i,
                'total': total_steps,
                'progress': progress,
                'status': f'正在下載... {progress}%'
            }
        )
        
        # 隨機模擬失敗（測試用）
        if random.random() < 0.1:  # 10% 失敗率
            raise Exception('下載過程中發生錯誤')
    
    # 任務完成
    return {
        'task_id': task_id,
        'url': url,
        'format': format,
        'quality': quality,
        'status': 'completed',
        'download_url': f'/downloads/{task_id}.{format}',
        'completed_at': datetime.now().isoformat()
    }

@celery_app.task
def test_task(x, y):
    """測試任務"""
    return {'result': x + y, 'operation': 'addition'}

@celery_app.task
def long_running_task():
    """長時間運行任務示例"""
    time.sleep(10)
    return {'status': 'done', 'message': '長時間任務完成'}
