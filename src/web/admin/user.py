from sqladmin import ModelView

from src.db.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]  # noqa: RUF012
