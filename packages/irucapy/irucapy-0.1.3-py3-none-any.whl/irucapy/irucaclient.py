from .irucaapi import IrucaAPI
from .memberupdate import MemberUpdateParam
from . import room, member, members
from typing import Optional


class IrucaClient:
    def __init__(self, room_code: str, api: IrucaAPI) -> None:
        """
        Represents one iruca room.

        Parameters
        ----------
        room_code : str
            The room code.
        api : IrucaAPI
            The instance of `IrucaAPI`.
        """
        self.room_code: str = room_code
        self.api: IrucaAPI = api

    def get_room_info(self) -> room.Room:
        """
        Call the `ルーム情報取得API`.
        Reference: https://iruca.co/api

        Returns
        -------
        room : Room

        Raises
        ------
        NetworkError
        RoomNotFoundError
        """
        return self.api.get_room_info(self.room_code)

    def get_room_members(self) -> members.Members:
        """
        Call the `メンバー一覧取得API`.
        Reference: https://iruca.co/api

        Returns
        -------
        members : Members

        Raises
        ------
        NetworkError
        RoomNotFoundError
        """
        return self.api.get_room_members(self.room_code)

    def get_room_member(self, member_id: int) -> member.Member:
        """
        Call the `メンバー情報取得API`.
        Reference: https://iruca.co/api

        Parameters
        ----------
        member_id : int

        Returns
        -------
        member : Member

        Raises
        ------
        NetworkError
        RoomNotFoundError
        """
        return self.api.get_room_member(self.room_code, member_id)

    def update_room_member(self, member_id: int, status: str, name: Optional[str] = None, message: Optional[str] = None) -> member.Member:
        """
        Call the `メンバー情報更新API`.
        Reference: https://iruca.co/api

        Parameters
        ----------
        member_id : int
        status : str
        name : Optional[str]
        message : Optional[str]

        Returns
        -------
        member : Member

        Raises
        ------
        NetworkError
        RoomNotFoundError
        """
        param: MemberUpdateParam = MemberUpdateParam(status, name, message)
        return self.api.update_room_member(self.room_code, member_id, param)
