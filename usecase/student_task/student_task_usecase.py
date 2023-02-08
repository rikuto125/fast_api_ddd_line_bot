from abc import ABC, abstractmethod
from typing import Optional, cast

import shortuuid

from domain.student_task.student_task import StudentTaskEntity
from domain.student_task.student_task_repsotory import StudentTaskRepository
from usecase.student_task.student_task_query_model import StudentTaskReadModel


class StudentTaskCommandUseCaseUnitOfWork(ABC):

    task_repository: StudentTaskRepository

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class StudentTaskCommandUseCase(ABC):
    """UserCommandUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def create_task(self, user_id:str, task_data:str) -> Optional[StudentTaskReadModel]:
        raise NotImplementedError

    def find_by_id(self, id: str) -> Optional[StudentTaskReadModel]:
        raise NotImplementedError

    def update(self, user: StudentTaskReadModel) -> None:
        raise NotImplementedError


class StudentTaskCommandUseCaseImpl(StudentTaskCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
            self,
            uow: StudentTaskCommandUseCaseUnitOfWork,
    ):
        self.uow: StudentTaskCommandUseCaseUnitOfWork = uow

    def create_task(self, user_id:str, task_data:str) -> Optional[StudentTaskReadModel]:
        try:
            uuid = shortuuid.uuid()
            task = StudentTaskEntity(
                id=uuid,
                line_user_id=user_id,
                task=task_data
            )

            self.uow.task_repository.create(task)
            self.uow.commit()

            created_task = self.uow.task_repository.find_by_id(uuid)

        except:
            self.uow.rollback()
            raise

        return StudentTaskReadModel.from_entity(cast(StudentTaskEntity, created_task))
