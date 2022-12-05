from enum import Enum
from typing import Optional

import strawberry
from experiment.scalars import ArrowType
from strawberry.schema_directive import Location

from .entity import UserEntity


@strawberry.schema_directive(locations=[Location.OBJECT])
class Keys:
    fields: str


@strawberry.type(directives=[Keys(fields="id")])
class User:
    username: str
    created_at: ArrowType
    updated_at: ArrowType
    password_modified_at: Optional[ArrowType]

    @classmethod
    def marshal(cls, user_entity: UserEntity) -> "User":
        # noinspection PyArgumentList
        return cls(
            username=user_entity.username,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
            password_modified_at=user_entity.password_modified_at,
        )


class UserRole(str, Enum):
    user = "user"
    admin = "admin"
