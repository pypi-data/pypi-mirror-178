from . import member, dataclassutil
from typing import List,Optional
import json
Members = List[member.Member]


def from_json_maybe(json_text: str) -> Optional[member.Member]:
    try:
        obj = []
        data = json.loads(json_text)
        for member_data in data:
            member_obj_maybe = member.from_json_object_maybe(member_data)
            if member_obj_maybe is not None:
                obj.append(member_obj_maybe)
        return obj
    except:
        return None