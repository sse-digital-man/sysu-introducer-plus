import sys; sys.path.append("./src/interface/live")

from utils.config import config
from .interface import CrawlerInterface, CrawlerCallback
from .kind import CrawlerKind
from .bilibili import BilibiliCrawler
from .virtual import VirtualCrawler

# 现在这里默认使用 Bilibili 直播进行部署
map = {
    CrawlerKind.Bilibili: BilibiliCrawler,
    CrawlerKind.Virtual: VirtualCrawler
}

def LiveCrawler(receive_callback: CrawlerCallback) -> CrawlerInterface:
    kind_text = config.get_use_module('llm', 'kind')

    try:
        kind = CrawlerKind(kind_text)
    except:
        raise KeyError("unknown kind of bot: {}".format(kind_text))
    
    return map[kind](receive_callback)