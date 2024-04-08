from typing import Dict, List
from .base import SearcherInterface

class ESSearcher(SearcherInterface):
    def search(self, query: str, size: int) -> List[str]:
        ...
    
    def search_with_label(self, query: str, size: int) -> Dict[str, str]:
        ...