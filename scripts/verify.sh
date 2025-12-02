#!/bin/bash

echo "🔍 驗證開發環境..."

# 1. 檢查 Python
echo "Python 版本: $(python3 --version)"
echo "Pip 版本: $(pip3 --version)"

# 2. 檢查 Node.js
echo "Node.js 版本: $(node --version)"
echo "NPM 版本: $(npm --version)"

# 3. 檢查 Docker
echo "Docker 版本: $(docker --version)"
echo "Docker Compose 版本: $(docker-compose --version)"

# 4. 檢查 Redis
redis-cli ping 2>/dev/null && echo "Redis: ✅ 運行中" || echo "Redis: ❌ 未運行"

# 5. 檢查虛擬環境
if [ -f "backend/venv/bin/activate" ]; then
    echo "Python 虛擬環境: ✅ 存在"
else
    echo "Python 虛擬環境: ❌ 不存在"
fi

# 6. 檢查依賴
echo "後端依賴:"
pip list | grep -E "(fastapi|yt-dlp|celery|redis)"

echo "前端依賴:"
npm list --depth=0 2>/dev/null | grep -E "(vue|axios|bootstrap)"

echo "✅ 驗證完成！"
