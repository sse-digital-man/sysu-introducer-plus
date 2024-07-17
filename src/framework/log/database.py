from utils.time import now_str
from utils.database import Database
from utils.file import dump_json

from . import ModuleLog


class LogDatabase(Database):
    def __init__(self):
        super().__init__("log", "content")

    def _create(self):
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS log (
                id INTEGER PRIMARY KEY autoincrement,
                log_kind TINYINT    NOT NULL,
                name TEXT,
                kind TEXT,
                time DATETIME   NOT NULL,
                content TEXT    NOT NULL
            )"""
        )

    def append(self, log: ModuleLog):
        self._conn.execute(
            "INSERT INTO log VALUES (?, ?, ?, ?, ?, ?)",
            (None, log.log_kind, log.name, log.kind, now_str(), dump_json(log.content)),
        )
        self._conn.commit()


DATABASE = LogDatabase()
