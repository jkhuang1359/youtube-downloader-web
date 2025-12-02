#!/bin/bash

echo "🔍 測試所有服務..."
echo "======================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 測試 Redis
echo -n "1. 測試 Redis (localhost:6380)... "
if redis-cli -p 6380 ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 正常${NC}"
else
    echo -e "${RED}❌ 失敗${NC}"
fi

# 測試後端 API
echo -n "2. 測試後端 API (localhost:8000)... "
if curl -s http://localhost:8000/ | grep -q "running"; then
    echo -e "${GREEN}✅ 正常${NC}"
else
    echo -e "${RED}❌ 失敗${NC}"
fi

# 測試 Celery 任務
echo -n "3. 測試 Celery 任務... "
TASK_RESPONSE=$(curl -s -X POST http://localhost:8000/api/test-celery 2>/dev/null)
if echo "$TASK_RESPONSE" | grep -q "task_id"; then
    TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"task_id":"[^"]*' | cut -d'"' -f4)
    echo -e "${GREEN}✅ 正常 (任務ID: ${TASK_ID})${NC}"
else
    echo -e "${RED}❌ 失敗${NC}"
fi

# 測試前端
echo -n "4. 測試前端 (localhost:8080)... "
if curl -s -I http://localhost:8080 | head -n1 | grep -q "200"; then
    echo -e "${GREEN}✅ 正常${NC}"
else
    echo -e "${RED}❌ 失敗${NC}"
fi

# 測試 API 文檔
echo -n "5. 測試 API 文檔 (localhost:8000/docs)... "
if curl -s http://localhost:8000/docs | grep -q "Swagger UI"; then
    echo -e "${GREEN}✅ 正常${NC}"
else
    echo -e "${RED}❌ 失敗${NC}"
fi

echo "======================"
echo -e "${GREEN}🎉 測試完成！${NC}"
echo ""
echo "📊 服務狀態："
echo "  • Redis:         localhost:6380"
echo "  • 後端 API:      http://localhost:8000"
echo "  • 前端應用:      http://localhost:8080"
echo "  • API 文檔:      http://localhost:8000/docs"
echo "  • Celery Worker: 運行中"
