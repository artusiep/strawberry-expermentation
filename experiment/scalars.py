from collections import UserString
from typing import NewType

import arrow
import strawberry
from experiment.graphql.context import SiepInfo

ArrowType = strawberry.scalar(
    NewType("ArrowType", arrow.Arrow), serialize=str, parse_value=arrow.get
)


class SiepPassword(UserString):
    def get_password_hash(self, info: SiepInfo):
        return info.context.pwd_context.hash(self)

    def verify_password(self, info: SiepInfo, hashed_password: str):
        return info.context.pwd_context.verify(self, hashed_password)


SiepPasswordType = strawberry.scalar(
    NewType("SiepPassword", SiepPassword), serialize=str, parse_value=SiepPassword
)
