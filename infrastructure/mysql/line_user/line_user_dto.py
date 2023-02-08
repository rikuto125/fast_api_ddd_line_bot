from datetime import datetime
from typing import Union
from sqlalchemy import Column, Integer, String


from domain.line_user.line_user import LineUserEntity
from driver.rdb import Base


def unixTimestamp() -> int:
    # 後で日本時間にする必要がある
    return int(datetime.now().timestamp())


class LineUserDTO(Base):
    __tablename__ = 'users'
    line_user_id: Union[str, Column] = Column(String(255), primary_key=True, index=True)
    user_name: Union[str, Column] = Column(String(255), nullable=False)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> LineUserEntity:
        return LineUserEntity(
            line_user_id=self.line_user_id,
            user_name=self.user_name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )



    @staticmethod
    def from_entity(user: LineUserEntity) -> "LineUserDTO":
        now = unixTimestamp()
        return LineUserDTO(
            line_user_id=user.line_user_id,
            name=user.user_name,
            created_at=now,
            updated_at=now,
        )
