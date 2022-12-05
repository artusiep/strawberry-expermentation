import strawberry
from sqlalchemy.exc import IntegrityError

from experiment.graphql.context import SiepInfo
from experiment.management.user.database import create_user
from experiment.management.user.mixin import PasswordConfirmMixin
from experiment.management.user.type import User, UserRole
from experiment.scalars import SiepPasswordType


@strawberry.type
class RegisterSuccess:
    user: User


@strawberry.type
class RegisterFailed:
    message: str


RegisterResult = strawberry.union("RegisterResult", (RegisterSuccess, RegisterFailed))


@strawberry.input
class RegisterInput(PasswordConfirmMixin):
    username: str
    password: SiepPasswordType
    password_confirm: SiepPasswordType

    def validate(self):
        return [self.validate_name(), self.validate_password(), self.validate_confirm()]

    def validate_name(self) -> str:
        if " " in self.username:
            return "Username must not contain a space."


async def register(info: SiepInfo, register_input: RegisterInput) -> RegisterResult:
    error_messages = [e for e in register_input.validate() if e is not None]
    if error_messages:
        return RegisterFailed(message=" ".join(error_messages))
    async with info.context.session_factory.begin() as session:
        try:
            user = await create_user(
                session,
                register_input.username,
                register_input.password.get_password_hash(info),
                [UserRole.user],
            )
        except IntegrityError:
            return RegisterFailed(message="Given username is already taken")
    return RegisterSuccess(user=User.marshal(user))
