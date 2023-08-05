from .types import ISO8601Text
from typing import Optional
from dataclasses import dataclass
from . import dataclassutil


@dataclass
class Member:
    """
    The response template for the `メンバー情報取得API`.
    Reference: https://iruca.co/api
    """
    id: int
    room_id: int
    name: str
    status: str
    message: str
    created_at: ISO8601Text
    updated_at: ISO8601Text
    position: int


def from_json_maybe(json_text: str) -> Optional[Member]:
    return dataclassutil.from_json_maybe(json_text, Member)
