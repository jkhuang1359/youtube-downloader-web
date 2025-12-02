#!/bin/bash

echo "🖥️  系統環境資訊收集"
echo "========================"

echo "📋 WSL 資訊:"
wsl --version 2>/dev/null || echo "WSL 版本指令不可用"

echo ""
echo "📋 Linux 資訊:"
echo "發行版: $(lsb_release -ds 2>/dev/null || cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "核心版本: $(uname -r)"
echo "架構: $(uname -m)"

echo ""
echo "📋 Python 資訊:"
python3 --version
pip --version 2>/dev/null || echo "pip 未安裝"

echo ""
echo "📋 Node.js 資訊:"
node --version
npm --version

echo ""
echo "📋 Docker 資訊:"
docker --version
docker-compose --version 2>/dev/null || echo "docker-compose 未安裝"

echo ""
echo "📋 記憶體與磁碟使用:"
free -h | grep -E "^Mem:" | awk '{print "記憶體: "$2" / "$3" 使用中"}'
df -h / | tail -1 | awk '{print "根目錄磁碟: "$2" / "$3" 使用中 ("$5")"}'

echo ""
echo "📋 已安裝的重要套件:"
echo "Python 全域套件:"
pip list --format=freeze 2>/dev/null | grep -E "(fastapi|celery|uvicorn|sqlalchemy|redis)" || echo "未找到相關套件"

echo ""
echo "Node.js 全域套件:"
npm list -g --depth=0 2>/dev/null | grep -E "(vue|npm|node)" || echo "未找到相關套件"

echo ""
echo "📋 網路資訊:"
echo "IP 地址: $(hostname -I 2>/dev/null | awk '{print $1}')"
echo "主機名: $(hostname)"
