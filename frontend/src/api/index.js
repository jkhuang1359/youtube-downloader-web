import axios from 'axios'

// 創建 axios 實例
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    // 可以在這裡添加 token 等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 回應攔截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const { response } = error
    
    if (response) {
      switch (response.status) {
        case 400:
          console.error('請求錯誤:', response.data)
          break
        case 401:
          console.error('未授權')
          // 可以跳轉到登入頁面
          break
        case 404:
          console.error('資源未找到')
          break
        case 500:
          console.error('伺服器錯誤')
          break
        default:
          console.error('未知錯誤')
      }
    }
    
    return Promise.reject(error)
  }
)

// API 方法
export const downloadApi = {
  // 開始下載
  startDownload(data) {
    return api.post('/api/v1/downloads', data)
  },
  
  // 獲取下載列表
  getDownloads(params = {}) {
    return api.get('/api/v1/downloads', { params })
  },
  
  // 獲取下載詳情
  getDownload(taskId) {
    return api.get(`/api/v1/downloads/${taskId}`)
  },
  
  // 測試 Celery
  testCelery() {
    return api.post('/api/v1/test-celery')
  }
}

export default api
