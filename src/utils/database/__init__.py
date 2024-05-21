import sqlite3
from abc import ABCMeta, abstractmethod
from utils.file import join_path

BASE_PATH = "data"


class Database(metaclass=ABCMeta):
    def __init__(self, path: str, database: str, check_same_thread: bool = False):
        name = join_path(BASE_PATH, path, database) + ".db"
        self._conn = sqlite3.connect(name, check_same_thread=check_same_thread)

        self._create()

    @abstractmethod
    def _create(self): ...
