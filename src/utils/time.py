from datetime import datetime


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def now() -> datetime:
    return datetime.now()


def sub_time(start: datetime, end: datetime) -> float:
    delta = end - start

    return delta.seconds + delta.microseconds / 1e6
