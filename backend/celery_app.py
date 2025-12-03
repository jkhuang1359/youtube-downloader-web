from celery import Celery
import os

# 創建 Celery 應用實例
celery_app = Celery(
    'youtube_downloader',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    include=['tasks']  # 包含 tasks 模塊中的任務
)

# 配置 Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30分鐘
    task_soft_time_limit=25 * 60,  # 25分鐘
)

# 如果有異步任務，在這裡配置
# 例如：celery_app.conf.beat_schedule = { ... }
