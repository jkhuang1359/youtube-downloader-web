#!/bin/bash

set -e

echo "🚀 啟動 YouTube Downloader 開發環境..."
echo "=========================================="

# 設置工作目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 清理函數
cleanup() {
    echo ""
    echo "🛑 停止所有服務..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $CELERY_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    docker stop redis-dev 2>/dev/null || true
    docker rm redis-dev 2>/dev/null || true
    echo "✅ 所有服務已停止"
    exit 0
}

# 捕獲 Ctrl+C 信號
trap cleanup INT

# 1. 啟動 Redis
echo "1️⃣  啟動 Redis 服務..."
docker stop redis-dev 2>/dev/null || true
docker rm redis-dev 2>/dev/null || true
docker run --name redis-dev -p 6380:6379 -d redis
sleep 2
echo "   ✅ Redis 已啟動 (localhost:6380)"

# 2. 啟動後端 API
echo "2️⃣  啟動後端 API 服務..."
cd "$BACKEND_DIR"
source venv/bin/activate

# 設置 Redis URL 環境變數
export REDIS_URL="redis://localhost:6380/0"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
sleep 3
echo "   ✅ 後端 API 已啟動 (http://localhost:8000)"

# 3. 啟動 Celery Worker
echo "3️⃣  啟動 Celery Worker..."
export REDIS_URL="redis://localhost:6380/0"
celery -A app.celery worker --loglevel=info --hostname=worker1@%h --pool=solo &
CELERY_PID=$!
sleep 2
echo "   ✅ Celery Worker 已啟動"

# 4. 啟動前端應用
echo "4️⃣  啟動前端應用..."
cd "$FRONTEND_DIR"

# 修復可能的 ESLint 錯誤
if command -v npx &> /dev/null; then
    npx eslint --fix src/App.vue 2>/dev/null || true
fi

npm run serve &
FRONTEND_PID=$!
sleep 5
echo "   ✅ 前端應用已啟動 (http://localhost:8080)"

# 顯示服務資訊
echo ""
echo "=========================================="
echo "🎉 所有服務啟動完成！"
echo ""
echo "📊 服務資訊："
echo "  • 後端 API:      http://localhost:8000"
echo "  • API 文檔:      http://localhost:8000/docs"
echo "  • 前端應用:      http://localhost:8080"
echo "  • Redis:         localhost:6380"
echo "  • Celery Worker: 運行中"
echo ""
echo "🔧 測試命令："
echo "  curl http://localhost:8000/              # 測試 API"
echo "  curl http://localhost:8000/api/test-celery # 測試 Celery"
echo "  redis-cli -p 6380 ping                   # 測試 Redis"
echo ""
echo "🛑 按 Ctrl+C 停止所有服務"
echo "=========================================="

# 等待所有後台進程
wait
