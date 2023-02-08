from abc import ABC, abstractmethod
from typing import Optional
from domain.student_task.student_task import StudentTaskEntity


class StudentTaskRepository(ABC):
    """BookRepository defines a repository interface for Book entity."""
    @abstractmethod
    def create(self, task: StudentTaskEntity) -> Optional[StudentTaskEntity]:
        raise NotImplementedError

    def find_by_id(self, id: str) -> Optional[StudentTaskEntity]:
        raise NotImplementedError

    def update(self, task: StudentTaskEntity) -> None:
        raise NotImplementedError

    def delete(self, id: str) -> None:
        raise NotImplementedError
