import strawberry
from experiment.graphql.permissions import AdminPermission, UserPermission
from strawberry.fastapi import GraphQLRouter
from strawberry.schema_directive import Location

from ..management.user.resolvers.change_password import (
    ChangePasswordResult,
    change_password,
)
from ..management.user.resolvers.get_user import get_user
from ..management.user.resolvers.get_users import get_users
from ..management.user.resolvers.login import LoginResult, login
from ..management.user.resolvers.register import RegisterResult, register
from ..management.user.resolvers.set_password import SetPasswordResult, set_password
from .context import get_context


@strawberry.type
class Management:
    users = strawberry.field(resolver=get_users, permission_classes=[AdminPermission])
    user = strawberry.field(resolver=get_user, permission_classes=[AdminPermission])


@strawberry.type
class Query:
    management: Management = strawberry.field(resolver=Management)


@strawberry.type
class ManagementMutations:
    login: LoginResult = strawberry.field(resolver=login)
    register: RegisterResult = strawberry.field(resolver=register)
    change_password: ChangePasswordResult = strawberry.field(
        resolver=change_password, permission_classes=[UserPermission]
    )
    set_password: SetPasswordResult = strawberry.field(
        resolver=set_password, permission_classes=[AdminPermission]
    )


@strawberry.type
class Mutation:
    management: ManagementMutations = strawberry.field(resolver=ManagementMutations)


@strawberry.schema_directive(locations=[Location.SCHEMA])
class Contact:
    name: str = strawberry.field(default="User Management System")


router = GraphQLRouter(
    strawberry.Schema(Query, mutation=Mutation, schema_directives=[Contact()]),
    graphiql=True,
    context_getter=get_context,
)
