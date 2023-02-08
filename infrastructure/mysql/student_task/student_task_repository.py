from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from domain.student_task.student_task import StudentTaskEntity
from infrastructure.mysql.student_task.student_task_dto import StudentTaskDTO
from usecase.student_task.student_task_usecase import StudentTaskCommandUseCaseUnitOfWork


class StudentTaskRepository:
    pass


class StudentTaskRepositoryImpl(StudentTaskRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[StudentTaskEntity]:
        try:
            line_task_dto = self.session.query(StudentTaskDTO).filter_by(id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return line_task_dto.to_entity()

    def create(self, task: StudentTaskEntity):
        line_task_dto = StudentTaskDTO.from_entity(task)
        try:
            self.session.add(line_task_dto)
        except:
            raise

    def update(self, task: StudentTaskEntity):
        line_task_dto = StudentTaskDTO.from_entity(task)
        try:
            _task = self.session.query(StudentTaskDTO).filter_by(id=line_task_dto.id).one()
            _task.line_user_id = line_task_dto.line_user_id
            _task.task_name = line_task_dto.task_name
            _task.created_at = line_task_dto.created_at
            _task.updated_at = line_task_dto.updated_at
        except:
            raise

    def delete(self, task: StudentTaskEntity):
        line_task_dto = StudentTaskDTO.from_entity(task)
        try:
            self.session.delete(line_task_dto)
        except:
            raise


class StudentTaskCommandUseCaseUnitOfWorkImpl(StudentTaskCommandUseCaseUnitOfWork):
    def __init__(
            self,
            session: Session,
            task_repository: StudentTaskRepository
    ):
        self.session = session
        self.task_repository: StudentTaskRepository = task_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
