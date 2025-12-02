# 問題記錄日誌

## 已解決的問題
### 問題 1: WSL 版本過舊
- **症狀**: Docker 提示 WSL 需要更新
- **解決**: 執行 `wsl --update` 更新到 2.6.1.0

### 問題 2: Python 依賴衝突
- **症狀**: SQLAlchemy 2.0.23 與 databases 0.7.0 衝突
- **解決**: 將 SQLAlchemy 降級到 1.4.47

### 問題 3: 前端 ESLint 錯誤
- **症狀**: 單引號/雙引號和分號格式錯誤
- **解決**: 使用 `eslint --fix` 自動修復

### 問題 4: Redis 端口衝突
- **症狀**: 6379 端口已被佔用
- **解決**: 改用 6380 端口

### 問題 5: Celery 找不到 app.tasks
- **症狀**: ModuleNotFoundError: No module named 'app.tasks'
- **解決**: 創建 tasks.py 和正確的導入結構

## 待解決的問題
無
