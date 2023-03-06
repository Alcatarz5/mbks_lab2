import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self, Callable

from sqlalchemy import create_engine, select, update
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.orm import Session

from database.db_models import User, Object

_log = logging.getLogger(__name__)
engine = create_engine('postgresql+psycopg2://postgres:post@localhost/mbks_lab1')


class Storage(ABC):
    def __init__(self) -> None:
        self._connected = False

    def __aenter__(self) -> Self:
        self.connect()
        return self

    def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @abstractmethod
    def connect(self) -> None:
        if self._connected:
            raise RuntimeError("Storage is already connected")
        self._connected = True
        _log.debug("Connected to storage %r", self)

    @abstractmethod
    def close(self) -> None:
        if not self._connected:
            raise RuntimeError("Storage is not connected")
        self._connected = False
        _log.debug("Closed connection to storage %r", self)

    @abstractmethod
    def create_user(self, u_name: str, u_access_mark: int) -> None:
        pass

    @abstractmethod
    def change_user_access_level(self, u_name: str, u_access_mark: int) -> None:
        pass

    @abstractmethod
    def user_exists(self, u_name: str) -> bool:
        pass

    @abstractmethod
    def get_user(self, u_name: str) -> str:
        pass

    @abstractmethod
    def create_object(self, o_name: str, o_user_id: int, o_secure_mark: int, o_file_uri: str) -> None:
        pass

    @abstractmethod
    def object_exist(self, o_name: str) -> bool:
        pass

    @abstractmethod
    def change_object_secure_level(self, o_name: str, o_secure_mark: int) -> None:
        pass

    @abstractmethod
    def change_object_owner(self, o_name: str, u_name: str) -> None:
        pass

    @abstractmethod
    def get_object(self, o_name) -> str:
        pass


class SQLAlchemyStorage(Storage):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        super().__init__()
        self._session_factory = session_factory
        self._session: Session | None = None

    def connect(self) -> None:
        super().connect()
        self._session = self._session_factory()
        self._session.begin()

    def close(self) -> None:
        super().close()
        if self._session is None:
            raise AssertionError("Storage is not connected")
        self._session.commit()
        self._session.close()
        self._session = None

    def create_user(self, u_name: str, u_access_mark: int) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        self._session.execute(
            Insert(User)
            .values(
                access_mark=u_access_mark,
                name=u_name
            )
        )

    def change_user_access_level(self, u_name: str, u_access_mark: int) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        self._session.execute(
            update(User)
            .values(
                access_mark=u_access_mark
            )
            .where(User.name == u_name)
        )

    def user_exists(self, u_name: str) -> bool:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = self._session.execute(
            select(User.id)
            .where(User.name == u_name)
        )
        return result.scalar_one_or_none() is not None

    def get_user(self, u_name: str) -> str:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = self._session.execute(
             select(User)
             .where(User.name == u_name)
        )
        return result.scalar_one_or_none()

    def create_object(self, o_name: str, o_user_id: int, o_secure_mark: int, o_file_uri: str) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        self._session.execute(
            Insert(Object)
            .values(
                user_id=o_user_id,
                secure_mark=o_secure_mark,
                file_uri=o_file_uri,
                name=o_name
            )
        )

    def object_exist(self, o_name: str) -> bool:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = self._session.execute(
            select(Object)
            .where(Object.name == o_name)
        )
        return result.scalar_one_or_none() is not None

    def change_object_owner(self, o_name: str, u_name: str) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        user_id = self.get_user(u_name=u_name).id
        self._session.execute(
            update(Object).
            values(
                user_id=user_id
            ).
            where(Object.name == o_name)
        )

    def change_object_secure_level(self, o_name: str, o_secure_mark: int) -> None:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        self._session.execute(
            update(Object)
            .values(
                secure_mark=o_secure_mark
            )
            .where(Object.name == o_name)
        )

    def get_object(self, o_name) -> str:
        if self._session is None:
            raise AssertionError("Storage is not connected")
        result = self._session.execute(
            select(Object)
            .where(Object.name == o_name)
        )
        return result.scalar_one_or_none()
