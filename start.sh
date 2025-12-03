#!/bin/bash
# start.sh - YouTube Downloader Web 启动脚本

echo "🚀 启动 YouTube Downloader Web..."

# 检查 docker-compose 是否可用
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: docker-compose 未安装"
    exit 1
fi

# 检查配置文件
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误: docker-compose.yml 文件不存在"
    exit 1
fi

# 清理旧的健康检查服务定义（如果需要）
echo "🔧 检查并清理配置..."
if grep -q "health-checker:" docker-compose.yml; then
    if [ ! -f "Dockerfile" ] && [ ! -f "Dockerfile.healthcheck" ]; then
        echo "⚠️  检测到 health-checker 服务但缺少 Dockerfile，将跳过构建..."
        # 创建临时副本，注释掉 health-checker
        cp docker-compose.yml docker-compose.yml.backup
        sed '/health-checker:/,/^  [a-z]/s/^/#/' docker-compose.yml > docker-compose.tmp
        mv docker-compose.tmp docker-compose.yml
    fi
fi

# 构建和启动服务
echo "📦 构建 Docker 镜像..."
docker-compose build --no-cache 2>&1 | grep -E "(Step|ERROR|failed)" || true

echo "🚀 启动容器..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo -e "\n=== 运行健康检查 ==="
if docker-compose ps backend | grep -q "Up"; then
    echo "在 backend 容器中运行健康检查..."

    # 确保依赖已安装
    echo "确保依赖已安装..."
    docker-compose exec backend pip install psycopg2-binary redis celery flower --quiet 2>/dev/null || true

    # 复制修复后的健康检查脚本（如果需要）
    if [ -f "health_check.py" ]; then
        docker cp health_check.py $(docker-compose ps -q backend):/app/health_check.py 2>/dev/null || true
    fi

    # 运行健康检查
    docker-compose exec backend python /app/health_check.py
else
    echo "❌ backend 服务未运行，跳过健康检查"
fi

# 显示服务信息
echo -e "\n=== API 端点 ==="
echo "Backend API: http://localhost:8000"
echo "Frontend:    http://localhost:3000"
echo "Flower:      http://localhost:5555"
echo "Database:    localhost:5432"
echo "Redis:       localhost:6379"

echo -e "\n✅ 服务启动完成！"
echo "📝 使用以下命令查看日志: docker-compose logs -f"
