import sys; sys.path.append("./src/interface/live")

from crawler import CrawlerInterface
from .bilibili import BilibiliCrawler

# 现在这里默认使用 Bilibili 直播进行部署
def get_live_crawler() -> CrawlerInterface:
    return BilibiliCrawler

LiveCrawler = get_live_crawler()