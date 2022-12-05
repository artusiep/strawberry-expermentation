import arrow
import strawberry
from experiment.graphql.context import SiepInfo
from experiment.management.user.database import change_user_password
from experiment.management.user.mixin import PasswordMixin
from experiment.management.user.type import User
from experiment.scalars import SiepPasswordType
from sqlalchemy.exc import NoResultFound


@strawberry.input
class SetPasswordInput(PasswordMixin):
    username: str
    password: SiepPasswordType

    def validate(self):
        return self.validate_password()


@strawberry.type
class SetPasswordSuccess:
    user: User


@strawberry.type
class SetPasswordFailed:
    message: str


SetPasswordResult = strawberry.union(
    "SetPasswordResult", (SetPasswordSuccess, SetPasswordFailed)
)


async def set_password(
    info: SiepInfo, change_password_input: SetPasswordInput
) -> SetPasswordResult:
    if error_message := change_password_input.validate():
        return SetPasswordFailed(message=error_message)
    async with info.context.session_factory.begin() as session:
        try:
            user = await change_user_password(
                session,
                change_password_input.username,
                change_password_input.password.get_password_hash(info),
                arrow.utcnow(),
            )
        except NoResultFound:
            return SetPasswordFailed(
                message=f"User with '{change_password_input.username}' username not found."
            )
    return SetPasswordSuccess(user=User.marshal(user))
