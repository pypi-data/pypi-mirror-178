from .types import UUIDText, ISO8601Text
from typing import Optional, List
from dataclasses import dataclass
from . import dataclassutil


@dataclass
class Room:
    """
    The response template for the `ルーム情報取得API`.
    Reference: https://iruca.co/api
    """
    id: int
    code: UUIDText
    name: str
    note: str
    statuses: List[str]
    created_at: ISO8601Text
    updated_at: ISO8601Text
    status_updated_at: ISO8601Text


def from_json_maybe(json_text: str) -> Optional[Room]:
    return dataclassutil.from_json_maybe(json_text, Room)