import pytest
import asyncio
from pathlib import Path
from app.core.downloader import YouTubeDownloader

class TestYouTubeDownloader:
    def setup_method(self):
        self.downloader = YouTubeDownloader(download_path="./test_downloads")
        
    def test_init(self):
        assert Path(self.downloader.download_path).exists()
        
    def test_get_video_info(self):
        # 測試獲取視頻信息
        pass
        
    def test_download_video(self):
        # 測試下載功能
        pass
        
if __name__ == "__main__":
    pytest.main()
