from .room import Room
from .member import Member
from .members import Members
from .memberupdate import MemberUpdateParam
from abc import ABC, abstractmethod


class IrucaAPI(ABC):
    """
    An interface of iruca API.
    Reference: https://iruca.co/api
    """
    @abstractmethod
    def get_room_info(self, room_code: str) -> Room:
        """
        Call the `ルーム情報取得API`.
        Reference: https://iruca.co/api

        Parameters
        ----------
        room_code : str

        Returns
        -------
        room : Room

        Raises
        ------
        NetworkError
        RoomNotFoundError
        """
        pass

    @abstractmethod
    def get_room_member(self, room_code: str, member_id: int) -> Member:
        """
        Call the `メンバー情報取得API`.
        Reference: https://iruca.co/api

        Parameters
        ----------
        room_code : str
        member_id : int

        Returns
        -------
        member : Member

        Raises
        ------
        NetworkError
        RoomNotFoundError
        """
        pass

    @abstractmethod
    def get_room_members(self, room_code: str) -> Members:
        """
        Call the `メンバー一覧取得API`.
        Reference: https://iruca.co/api

        Parameters
        ----------
        room_code : str

        Returns
        -------
        members : Members

        Raises
        ------
        NetworkError
        RoomNotFoundError
        MemberNotFoundError
        """
        pass

    @abstractmethod
    def update_room_member(self, room_code: str, member_id: int, param: MemberUpdateParam) -> None:
        """
        Call the `メンバー情報更新API`.
        Reference : https://iruca.co/api

        Parameters
        ----------
        room_code : str
        member_id : int
        param : MemberUpdateParam

        Raises
        ------
        NetworkError
        RoomNotFoundError
        MemberNotFoundError
        """
