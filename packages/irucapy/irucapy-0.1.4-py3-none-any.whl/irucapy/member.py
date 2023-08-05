from .types import ISO8601Text
from typing import Optional
from dataclasses import dataclass
from . import dataclassutil
import json


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
    message: Optional[str]
    created_at: ISO8601Text
    updated_at: ISO8601Text
    position: int


def from_json_maybe(json_text: str) -> Optional[Member]:
    return from_json_object_maybe(json.loads(json_text))


def from_json_object_maybe(o: object) -> Optional[Member]:
    try:
        return Member(
            id=o["id"],
            room_id=o["room_id"],
            name=o["name"],
            status=o["status"],
            message=o["message"],
            created_at=o["created_at"],
            updated_at=o["updated_at"],
            position=o["position"],
        )
    except:
        return None
