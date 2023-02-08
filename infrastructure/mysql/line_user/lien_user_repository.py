from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from domain.line_user.line_user import LineUserEntity
from infrastructure.mysql.line_user import LineUserDTO
from usecase.line_user.line_user_usecase import LineUserCommandUseCaseUnitOfWork


class LineUserRepository:
    pass


class LineUserRepositoryImpl(LineUserRepository):

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, id: str) -> Optional[LineUserEntity]:
        try:
            line_user_dto = self.session.query(LineUserDTO).filter_by(line_user_id=id).one()
        except NoResultFound:
            return None
        except:
            raise

        return line_user_dto.to_entity()

    def create(self, user: LineUserEntity):
        line_user_dto = LineUserDTO.from_entity(user)
        try:
            self.session.add(line_user_dto)
        except:
            raise

    def update(self, user: LineUserEntity):
        line_user_dto = LineUserDTO.from_entity(user)
        try:
            _user = self.session.query(LineUserDTO).filter_by(id=line_user_dto.id).one()
            _user.line_user_id = line_user_dto.line_user_id
            _user.user_name = line_user_dto.user_name
            _user.pub_date = line_user_dto.pub_date
            _user.created_at = line_user_dto.created_at
            _user.updated_at = line_user_dto.updated_at
        except:
            raise

    def delete(self, user: LineUserEntity):
        line_user_dto = LineUserDTO.from_entity(user)
        try:
            self.session.delete(line_user_dto)
        except:
            raise


class LineUserCommandUseCaseUnitOfWorkImpl(LineUserCommandUseCaseUnitOfWork):

    def __init__(
            self,
            session: Session,
            user_repository: LineUserRepository
    ):
        self.session = session
        self.user_repository: LineUserRepository = user_repository

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
