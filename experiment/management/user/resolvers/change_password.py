import arrow
import strawberry
from experiment.graphql.context import SiepInfo
from experiment.management.user.database import change_user_password
from experiment.management.user.mixin import PasswordConfirmMixin
from experiment.management.user.type import User


class ChangePasswordInput(PasswordConfirmMixin):
    def validate(self):
        return [self.validate_password(), self.validate_confirm()]


@strawberry.type
class ChangePasswordSuccess:
    user: User


@strawberry.type
class ChangePasswordFailed:
    message: str


ChangePasswordResult = strawberry.union(
    "ChangePasswordResult", (ChangePasswordSuccess, ChangePasswordFailed)
)


async def change_password(
    info: SiepInfo, change_password_input: ChangePasswordInput
) -> ChangePasswordResult:
    error_messages = [e for e in change_password_input.validate() if e is not None]
    if error_messages:
        return ChangePasswordFailed(message=" ".join(error_messages))
    async with info.context.session_factory.begin() as session:
        user = await change_user_password(
            session,
            info.context.request.state.user.username,
            change_password_input.password.get_password_hash(info),
            arrow.utcnow(),
        )
        return ChangePasswordSuccess(user=User.marshal(user))
