#!/bin/bash

echo "🔒 安全性檢查"
echo "======================"

# 檢查後端依賴安全性
echo "1. 檢查 Python 依賴安全性..."
cd backend
pip list --outdated 2>/dev/null | grep -E "(celery|redis|fastapi|sqlalchemy)"

# 檢查前端依賴安全性
echo ""
echo "2. 檢查 Node.js 依賴安全性..."
cd ../frontend
npm audit 2>/dev/null || echo "npm audit 不可用"

# 檢查環境變數
echo ""
echo "3. 檢查環境變數安全性..."
if [ -f "../backend/.env" ]; then
    echo "後端 .env 檔案存在"
    grep -E "(SECRET|KEY|PASSWORD|TOKEN)" ../backend/.env 2>/dev/null | \
        awk '{print substr($0,1,20)"..."}'
fi

echo ""
echo "4. 檢查端口安全性..."
netstat -tulpn 2>/dev/null | grep -E "(8000|8080|6380)" || echo "端口檢查失敗"

echo ""
echo "📋 建議:"
echo "1. 定期更新依賴套件"
echo "2. 不要在 .env 中提交敏感資訊"
echo "3. 使用環境變數管理密鑰"
echo "4. 定期執行安全性掃描"
