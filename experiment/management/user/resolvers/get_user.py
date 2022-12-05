import strawberry
from experiment.graphql.context import SiepInfo
from experiment.management.user.database import query_user
from experiment.management.user.type import User
from sqlalchemy.exc import NoResultFound


@strawberry.type
class GetUserSuccess:
    user: User


@strawberry.type
class GetUserFailed:
    message: str


GetUserResult = strawberry.union("GetUserResult", (GetUserSuccess, GetUserFailed))


async def get_user(info: SiepInfo, username: str) -> GetUserResult:
    async with info.context.session_factory.begin() as session:
        try:
            user = await query_user(session, username)
        except NoResultFound:
            return GetUserFailed(message=f"User with '{username}' username not found.")
        return GetUserSuccess(user=User.marshal(user))
