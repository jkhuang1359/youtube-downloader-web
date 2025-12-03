#!/usr/bin/env python3
"""
YouTube Downloader Web 健康檢查模塊
用於各服務的基礎功能檢測
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict

class HealthChecker:
    def __init__(self, log_dir: str = "tests/logs", environment: str = "docker"):
        """
        environment: "docker" 或 "host"
        - "docker": 在 Docker 容器中使用，使用容器名稱作為主機名
        - "host": 在宿主機中使用，使用 localhost 作為主機名
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"health_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "overall": "UNKNOWN"
        }
        
        # 根據環境設置默認主機名
        self.environment = environment.lower()
        
        if self.environment == "docker":
            # 在 Docker 容器內使用容器名稱
            self.default_db_host = "db"
            self.default_redis_host = "redis"
            self.default_api_url = "http://backend:8000"
            self.default_flower_url = "http://flower:5555"
            self.default_frontend_url = "http://frontend:3000"
        else:
            # 在宿主機或本地使用 localhost
            self.default_db_host = "localhost"
            self.default_redis_host = "localhost"
            self.default_api_url = "http://localhost:8000"
            self.default_flower_url = "http://localhost:5555"
            self.default_frontend_url = "http://localhost:3000"
        
        self.log(f"健康檢查初始化完成 - 環境: {self.environment}")
        self.log(f"數據庫主機: {self.default_db_host}")
        self.log(f"Redis主機: {self.default_redis_host}")
        self.log(f"API URL: {self.default_api_url}")
        self.log(f"Flower URL: {self.default_flower_url}")
        self.log(f"前端 URL: {self.default_frontend_url}")
    
    def log(self, message: str, level: str = "INFO"):
        """記錄日誌"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        
        print(log_message)
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")
            
        # 同時寫入主日誌
        main_log = os.path.join(self.log_dir, "health_check.log")
        with open(main_log, 'a') as f:
            f.write(log_message + "\n")
    
    def check_database(self) -> Dict:
        """檢查數據庫連接"""
        self.log("檢查數據庫連接...")
        start_time = time.time()
        
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', self.default_db_host),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'youtube_downloader'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres')
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT version(), NOW()")
            db_version, db_time = cursor.fetchone()
            
            cursor.execute("SELECT 1")
            test_result = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            elapsed = time.time() - start_time
            
            result = {
                "status": "HEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "version": db_version.split(",")[0],
                "details": f"連接正常，測試查詢返回: {test_result}"
            }
            self.log(f"數據庫檢查通過: {result['version']}")
            
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                "status": "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "error": str(e),
                "details": f"數據庫連接失敗 (主機: {os.getenv('DB_HOST', self.default_db_host)})"
            }
            self.log(f"數據庫檢查失敗: {e}", "ERROR")
        
        return result
    
    def check_redis(self) -> Dict:
        """檢查 Redis 連接"""
        self.log("檢查 Redis 連接...")
        start_time = time.time()
        
        try:
            import redis
            r = redis.Redis(
                host=os.getenv('REDIS_HOST', self.default_redis_host),
                port=int(os.getenv('REDIS_PORT', '6379')),
                db=int(os.getenv('REDIS_DB', '0'))
            )
            
            ping_result = r.ping()
            
            test_key = f"health_check_{int(time.time())}"
            r.set(test_key, "test_value", ex=10)
            read_value = r.get(test_key)
            r.delete(test_key)
            
            elapsed = time.time() - start_time
            
            result = {
                "status": "HEALTHY" if ping_result and read_value == b"test_value" else "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "ping": ping_result,
                "read_write_test": read_value == b"test_value",
                "details": "Redis 連接和讀寫測試正常" if ping_result else "Redis 連接失敗"
            }
            
            if result["status"] == "HEALTHY":
                self.log("Redis 檢查通過")
            else:
                self.log(f"Redis 檢查失敗: ping={ping_result}, read_write={read_value == b'test_value'}", "ERROR")
                
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                "status": "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "error": str(e),
                "details": f"Redis 連接失敗 (主機: {os.getenv('REDIS_HOST', self.default_redis_host)})"
            }
            self.log(f"Redis 檢查失敗: {e}", "ERROR")
        
        return result
    
    def check_backend_api(self) -> Dict:
        """檢查後端 API"""
        self.log("檢查後端 API...")
        start_time = time.time()
        
        try:
            import requests
            base_url = os.getenv('API_URL', self.default_api_url)
            
            health_response = requests.get(f"{base_url}/health", timeout=5)
            health_data = health_response.json() if health_response.status_code == 200 else {}
            
            api_response = requests.get(f"{base_url}/api/download/test", timeout=5)
            api_data = api_response.json() if api_response.status_code == 200 else {}
            
            elapsed = time.time() - start_time
            
            result = {
                "status": "HEALTHY" if health_response.status_code == 200 and api_response.status_code == 200 else "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "health_status": health_response.status_code,
                "api_status": api_response.status_code,
                "health_data": health_data,
                "api_data": api_data,
                "details": f"API 響應正常，健康端點: {health_response.status_code}, API端點: {api_response.status_code}"
            }
            
            if result["status"] == "HEALTHY":
                self.log(f"後端 API 檢查通過: {health_data.get('status', 'unknown')}")
            else:
                self.log(f"後端 API 檢查失敗: health={health_response.status_code}, api={api_response.status_code}", "ERROR")
                
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                "status": "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "error": str(e),
                "details": f"API 連接失敗 (URL: {os.getenv('API_URL', self.default_api_url)})"
            }
            self.log(f"後端 API 檢查失敗: {e}", "ERROR")
        
        return result
    
    def check_celery(self) -> Dict:
        """檢查 Celery"""
        self.log("檢查 Celery 服務...")
        start_time = time.time()
        
        try:
            import sys
            sys.path.insert(0, '/app')
            
            from celery_app import celery_app
            
            from celery import current_app
            
            inspect = current_app.control.inspect()
            stats = inspect.stats() or {}
            
            elapsed = time.time() - start_time
            
            active_workers = len(stats)
            
            result = {
                "status": "HEALTHY" if active_workers > 0 else "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "active_workers": active_workers,
                "workers": list(stats.keys()),
                "details": f"找到 {active_workers} 個活動的 Celery worker" if active_workers > 0 else "未找到活動的 Celery worker"
            }
            
            if result["status"] == "HEALTHY":
                self.log(f"Celery 檢查通過: {active_workers} 個 worker 運行中")
            else:
                self.log("Celery 檢查失敗: 沒有活動的 worker", "ERROR")
                
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                "status": "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "error": str(e),
                "details": "Celery 檢查失敗"
            }
            self.log(f"Celery 檢查失敗: {e}", "ERROR")
        
        return result
    
    def check_flower(self, max_retries: int = 3, retry_delay: int = 5) -> Dict:
        """檢查 Flower 監控，帶重試機制"""
        self.log("檢查 Flower 監控...")
        
        last_exception = None
        
        for attempt in range(max_retries):
            start_time = time.time()
            
            try:
                import requests
                flower_url = os.getenv('FLOWER_URL', self.default_flower_url)
                
                response = requests.get(flower_url, timeout=10)
                elapsed = time.time() - start_time
                
                result = {
                    "status": "HEALTHY" if response.status_code == 200 else "UNHEALTHY",
                    "response_time": f"{elapsed:.3f}s",
                    "http_status": response.status_code,
                    "details": f"Flower 監控正常 (HTTP {response.status_code})" if response.status_code == 200 else f"Flower 監控異常 (HTTP {response.status_code})"
                }
                
                if result["status"] == "HEALTHY":
                    self.log("Flower 檢查通過")
                    return result
                else:
                    last_exception = f"HTTP {response.status_code}"
                    
            except Exception as e:
                elapsed = time.time() - start_time
                last_exception = str(e)
                self.log(f"Flower 檢查嘗試 {attempt + 1}/{max_retries} 失敗: {e}", "WARNING")
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
        
        result = {
            "status": "UNHEALTHY",
            "response_time": f"{elapsed:.3f}s",
            "error": last_exception,
            "details": f"Flower 連接失敗 (URL: {os.getenv('FLOWER_URL', self.default_flower_url)})"
        }
        self.log(f"Flower 檢查失敗: {last_exception}", "ERROR")
        return result
    
    def check_frontend(self) -> Dict:
        """檢查前端服務"""
        self.log("檢查前端服務...")
        start_time = time.time()
        
        try:
            import requests
            frontend_url = os.getenv('FRONTEND_URL', self.default_frontend_url)
            
            response = requests.get(frontend_url, timeout=10)
            elapsed = time.time() - start_time
            
            is_html = 'text/html' in response.headers.get('Content-Type', '')
            
            result = {
                "status": "HEALTHY" if response.status_code in [200, 304] and is_html else "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "http_status": response.status_code,
                "content_type": response.headers.get('Content-Type', 'unknown'),
                "is_html": is_html,
                "details": f"前端服務正常 (HTTP {response.status_code})" if response.status_code in [200, 304] else f"前端服務異常 (HTTP {response.status_code})"
            }
            
            if result["status"] == "HEALTHY":
                self.log("前端檢查通過")
            else:
                self.log(f"前端檢查失敗: HTTP {response.status_code}, HTML: {is_html}", "ERROR")
                
        except Exception as e:
            elapsed = time.time() - start_time
            result = {
                "status": "UNHEALTHY",
                "response_time": f"{elapsed:.3f}s",
                "error": str(e),
                "details": f"前端連接失敗 (URL: {os.getenv('FRONTEND_URL', self.default_frontend_url)})"
            }
            self.log(f"前端檢查失敗: {e}", "ERROR")
        
        return result
    
    def run_all_checks(self) -> Dict:
        """運行所有健康檢查"""
        self.log("開始全面健康檢查...")
        
        checks = {
            "database": self.check_database,
            "redis": self.check_redis,
            "backend_api": self.check_backend_api,
            "celery": self.check_celery,
            "flower": self.check_flower,
            "frontend": self.check_frontend
        }
        
        all_healthy = True
        
        for service_name, check_func in checks.items():
            self.log(f"\n檢查 {service_name}...")
            result = check_func()
            self.results["services"][service_name] = result
            
            if result["status"] != "HEALTHY":
                all_healthy = False
        
        self.results["overall"] = "HEALTHY" if all_healthy else "UNHEALTHY"
        self.results["summary"] = {
            "total_services": len(checks),
            "healthy_services": sum(1 for s in self.results["services"].values() if s["status"] == "HEALTHY"),
            "unhealthy_services": sum(1 for s in self.results["services"].values() if s["status"] != "HEALTHY")
        }
        
        result_file = os.path.join(self.log_dir, f"health_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(result_file, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"\n健康檢查完成！結果已保存到: {result_file}")
        self.log(f"總體狀態: {self.results['overall']}")
        self.log(f"健康服務: {self.results['summary']['healthy_services']}/{self.results['summary']['total_services']}")
        
        return self.results
    
    def print_summary(self):
        """打印檢查總結"""
        print("\n" + "="*60)
        print("YouTube Downloader Web 健康檢查報告")
        print("="*60)
        print(f"檢查時間: {self.results['timestamp']}")
        print(f"總體狀態: {self.results['overall']}")
        print(f"健康服務: {self.results['summary']['healthy_services']}/{self.results['summary']['total_services']}")
        print("-"*60)
        
        for service_name, result in self.results["services"].items():
            status_icon = "✅" if result["status"] == "HEALTHY" else "❌"
            print(f"{status_icon} {service_name.upper():12} {result['status']:10} {result.get('response_time', 'N/A'):8} {result.get('details', '')}")
        
        print("="*60)
        
        if self.results["overall"] != "HEALTHY":
            print("\n🔧 問題服務建議:")
            for service_name, result in self.results["services"].items():
                if result["status"] != "HEALTHY":
                    print(f"  • {service_name}: {result.get('error', result.get('details', '未知錯誤'))}")
            
            print("\n🔄 建議操作:")
            print("  1. 檢查服務是否啟動: docker-compose ps")
            print("  2. 查看服務日誌: docker-compose logs [service_name]")
            print("  3. 重啟服務: docker-compose restart [service_name]")
            print("  4. 查看詳細日誌: cat tests/logs/health_check.log")

if __name__ == "__main__":
    # 自動檢測是否在 Docker 容器中
    in_docker = os.path.exists('/.dockerenv')
    environment = "docker" if in_docker else "host"
    
    checker = HealthChecker(environment=environment)
    checker.run_all_checks()
    checker.print_summary()
    
    sys.exit(0 if checker.results["overall"] == "HEALTHY" else 1)