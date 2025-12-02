#!/bin/bash

echo "📊 系統性能監控"
echo "======================"

while true; do
    echo "$(date '+%Y-%m-%d %H:%M:%S')"
    echo "CPU 使用率: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
    echo "記憶體使用: $(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')"
    echo "磁碟使用: $(df -h / | awk 'NR==2{print $5}')"
    
    # 檢查服務狀態
    echo -n "Redis: "
    redis-cli -p 6380 ping 2>/dev/null && echo "✅" || echo "❌"
    
    echo -n "後端 API: "
    curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy" && echo "✅" || echo "❌"
    
    echo "======================"
    sleep 30
done
