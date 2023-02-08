from abc import ABC, abstractmethod
from typing import Optional

from domain.line_user.line_user import LineUserEntity


class Line_UserRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""

    @abstractmethod
    def create(self, user: LineUserEntity) -> Optional[LineUserEntity]:
        raise NotImplementedError

    def find_by_id(self, id: str) -> Optional[LineUserEntity]:
        raise NotImplementedError

    def update(self, user: LineUserEntity) -> None:
        raise NotImplementedError
