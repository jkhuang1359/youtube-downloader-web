import os
from dotenv import load_dotenv

load_dotenv()

# Redis 配置 - 使用 6380 端口
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6380/0")

# 其他配置
DEBUG = True
SECRET_KEY = "your-secret-key-here"
