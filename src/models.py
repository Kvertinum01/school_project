from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import PrimaryKeyConstraint

Base = declarative_base()

class UsersTable(Base):
    __tablename__ = "users_table"
    __table_args__ = (
        PrimaryKeyConstraint('id', 'class_letter', 'class_num'),
    )
    __mapper_args__ = {"eager_defaults": True}

    user_id = Column("id", Integer, unique=True)
    class_letter = Column("class_letter", String)
    class_num = Column("class_num", Integer)

    def __init__(self, user_id: int, class_letter: str, class_num: int):
        self.user_id = user_id
        self.class_letter = class_letter
        self.class_num = class_num

    def __repr__(self) -> str:
        return "UserTable({}, {}, {})" \
            .format(self.user_id, self.class_letter, self.class_num)