#!/bin/bash

echo "=== 服務健康檢查 ==="

# 檢查 Redis
echo "1. 檢查 Redis..."
if redis-cli -p 6380 ping 2>/dev/null | grep -q PONG; then
    echo "   ✅ Redis (6380): 正常"
else
    echo "   ❌ Redis (6380): 異常"
fi

# 檢查後端 API
echo "2. 檢查後端 API..."
if curl -s http://localhost:8000/ | grep -q "running"; then
    echo "   ✅ 後端 API (8000): 正常"
else
    echo "   ❌ 後端 API (8000): 異常"
fi

# 檢查前端
echo "3. 檢查前端..."
if curl -s -I http://localhost:8080 | head -1 | grep -q "200"; then
    echo "   ✅ 前端 (8080): 正常"
else
    echo "   ❌ 前端 (8080): 異常"
fi

# 檢查 Celery
echo "4. 檢查 Celery Worker..."
cd backend
source venv/bin/activate
if celery -A app.celery inspect ping 2>/dev/null | grep -q "pong"; then
    echo "   ✅ Celery Worker: 正常"
else
    echo "   ❌ Celery Worker: 異常"
fi
cd ..

echo "=== 檢查完成 ==="
