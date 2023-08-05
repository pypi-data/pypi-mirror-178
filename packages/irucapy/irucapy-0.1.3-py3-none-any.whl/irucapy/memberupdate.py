from dataclasses import dataclass
from typing import Optional

@dataclass
class MemberUpdateParam:
    status : str
    name : Optional[str]
    message : Optional[str]