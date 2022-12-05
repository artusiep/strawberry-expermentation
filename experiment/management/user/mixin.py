import strawberry
from experiment.scalars import SiepPasswordType


@strawberry.input
class PasswordMixin:
    password: SiepPasswordType

    def validate_password(self) -> str:
        if len(self.password) < 8:
            return "Password is too short."


@strawberry.input
class PasswordConfirmMixin(PasswordMixin):
    password_confirm: SiepPasswordType

    def validate_confirm(self):
        if self.password_confirm != self.password:
            return "Passwords do not match."
