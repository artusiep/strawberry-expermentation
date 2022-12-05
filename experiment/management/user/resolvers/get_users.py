from experiment.graphql.context import SiepInfo
from experiment.management.user.database import query_users
from experiment.management.user.type import User


async def get_users(info: SiepInfo) -> list[User]:
    async with info.context.session_factory.begin() as session:
        users = await query_users(session)
        return [User.marshal(user) for user in users]
