const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,  // 固定使用 8080 端口
    host: 'localhost',
    hot: true,
    open: false,  // 不要自動打開瀏覽器
  },
  lintOnSave: 'warning'  // 將 lint 錯誤改為警告，不阻止編譯
})
