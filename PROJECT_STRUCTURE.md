# YouTube Downloader Web 專案結構

## 系統環境
- **WSL 2**: Ubuntu 22.04
- **Python**: 3.10.x
- **Node.js**: 18.x
- **Docker**: 24.x
- **Redis**: 7.x (Docker 容器)

## 開發環境設置
- **Redis**: Docker 容器，端口 6380
- **後端 API**: FastAPI，端口 8000
- **前端開發伺服器**: Vue CLI，端口 8080
- **Celery Worker**: 異步任務處理

## 依賴版本
- **後端**:
  - FastAPI: 0.104.1
  - Celery: 5.6.0
  - SQLAlchemy: 2.0.23
  - Redis 客戶端: 5.0.1

- **前端**:
  - Vue.js: 3.3.4
  - Vue Router: 4.2.4
  - Pinia: 2.1.7
  - Axios: 1.6.0
  - Bootstrap: 5.3.2
