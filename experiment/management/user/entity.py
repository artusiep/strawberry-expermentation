import arrow
from sqlalchemy import VARCHAR, Integer, ARRAY
from sqlalchemy.sql.schema import Column
from sqlalchemy_utils import ArrowType

from ...db.base import Base


class UserEntity(Base):
    __tablename__ = "user"

    id_ = Column("id", Integer(), primary_key=True, autoincrement=True)
    username = Column("username", VARCHAR(), nullable=False, unique=True)
    password = Column("password", VARCHAR(), nullable=False)
    created_at = Column("created_at", ArrowType, nullable=False, default=arrow.utcnow())
    updated_at = Column(
        "updated_at",
        ArrowType,
        nullable=False,
        default=arrow.utcnow(),
        onupdate=arrow.utcnow(),
    )
    password_modified_at = Column("password_modified_at", ArrowType, nullable=True)
    roles = Column("roles", ARRAY(VARCHAR()), nullable=False)
