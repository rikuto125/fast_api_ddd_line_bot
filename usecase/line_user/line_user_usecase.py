from abc import ABC, abstractmethod
from typing import Optional, cast
import shortuuid
from domain.line_user.line_user import LineUserEntity
from domain.line_user.line_user_repsotory import Line_UserRepository
from usecase.line_user.line_user_command_model import LineUserCreateModel
from usecase.line_user.line_user_query_model import LineUserReadModel


class LineUserCommandUseCaseUnitOfWork(ABC):
    """UserCommandUseCaseUnitOfWork defines an interface based on Unit of Work pattern."""

    user_repository: Line_UserRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class LineUserCommandUseCase(ABC):
    """UserCommandUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def create_user(self, user_id:str,profile:str) -> Optional[LineUserReadModel]:
        raise NotImplementedError
    #
    # def create_user(self, user_id: str, name:str)-> Optional[LineUserReadModel]:
    #     raise NotImplementedError

    def find_by_id(self, id: str) -> Optional[LineUserReadModel]:
        raise NotImplementedError

    def update(self, user: LineUserReadModel) -> None:
        raise NotImplementedError


class LineUserCommandUseCaseImpl(LineUserCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""
    def __init__(
            self,
            uow: LineUserCommandUseCaseUnitOfWork,
    ):
        self.uow: LineUserCommandUseCaseUnitOfWork = uow

    def create_user(self, user_id:str,profile:str) -> Optional[LineUserReadModel]:
        try:
            user = LineUserEntity(
                line_user_id=user_id,
                user_name=profile
            )

            existing_user = self.uow.user_repository.find_by_id(user.line_user_id)
            if existing_user is not None:
                raise ValueError("User already exists")

            self.uow.user_repository.create(user)
            self.uow.commit()

            created_user = self.uow.user_repository.find_by_id(user.line_user_id)

        except:
            self.uow.rollback()
            raise

        return LineUserReadModel.from_entity(cast(LineUserEntity, created_user))
