from . import room, member, members
from .exceptions import NetworkError, RoomNotFoundError, MemberNotFoundError
from .memberupdate import MemberUpdateParam
from .irucaapi import IrucaAPI
from urllib.request import urlopen, Request
import json
from dataclasses import asdict


class HTTPIrucaAPI(IrucaAPI):
    """
    An implementation of `IrucaAPI`.
    """

    def __init__(self) -> None:
        super().__init__()

    def get_room_url(self, room_code: str) -> str:
        """
        Get the URL of the room.

        Parameters
        ----------
        room_code : str
            The room code.

        Returns
        -------
        url : str
            The URL of the room.
        """
        return f"https://iruca.co/api/rooms/{room_code}"

    def get_room_info(self, room_code: str) -> room.Room:
        url: str = self.get_room_url(room_code)
        try:
            with urlopen(url) as res:
                data: bytes = res.read()
                json_text = data.decode("utf-8")
                room_data: room.Room | None = room.from_json_maybe(json_text)
                if room_data is None:
                    raise RoomNotFoundError()
                return room_data
        except Exception as e:
            if hasattr(e, "code") and e.code == 404:
                raise RoomNotFoundError(e)
            raise NetworkError(e)

    def get_room_members(self, room_code: str) -> members.Members:
        url: str = f"{self.get_room_url(room_code)}/members"
        try:
            with urlopen(url) as res:
                data: bytes = res.read()
                json_text = data.decode("utf-8")
                member_data: members.Members | None = members.from_json_maybe(
                    json_text)
                if member_data is None:
                    raise MemberNotFoundError()
                return member_data
        except Exception as e:
            if hasattr(e, "code") and e.code == 404:
                raise RoomNotFoundError(e)
            raise NetworkError(e)

    def get_room_member(self, room_code: str, member_id: int) -> member.Member:
        url: str = f"{self.get_room_url(room_code)}/members/{member_id}"
        try:
            with urlopen(url) as res:
                data: bytes = res.read()
                json_text = data.decode("utf-8")
                member_data: member.Member | None = member.from_json_maybe(
                    json_text)
                if member_data is None:
                    raise MemberNotFoundError()
                return member_data
        except Exception as e:
            if hasattr(e, "code") and e.code == 404:
                raise MemberNotFoundError(e)
            raise NetworkError(e)

    def update_room_member(self, room_code: str, member_id: int, param: MemberUpdateParam) -> None:
        url: str = f"{self.get_room_url(room_code)}/members/{member_id}"
        try:
            data = json.dumps(asdict(param)).encode()
            request = Request(url, data=data, headers={
                              "Content-Type": "application/json"}, method="PUT")
            with urlopen(request) as res:
                pass
        except Exception as e:
            if hasattr(e, "code") and e.code == 404:
                raise MemberNotFoundError(e)
            raise NetworkError(e)
