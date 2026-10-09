from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from .db.user_queries import get_user_by_username, get_user_by_id


class RawSQLAuthBackend:
    """
    Custom authentication backend using Raw SQL
    instead of Django ORM queries.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        user_data = get_user_by_username(username)

        if not user_data:
            return None

        if not user_data["is_active"]:
            return None

        if not check_password(password, user_data["password"]):
            return None

        User = get_user_model()

        user = User(
            id=user_data["id"],
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_staff=user_data["is_staff"],
            is_active=user_data["is_active"],
            is_superuser=user_data["is_superuser"],
            date_joined=user_data["date_joined"],
        )

        return user

    def get_user(self, user_id):
        user_data = get_user_by_id(user_id)

        if not user_data:
            return None

        if not user_data["is_active"]:
            return None

        User = get_user_model()

        user = User(
            id=user_data["id"],
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_staff=user_data["is_staff"],
            is_active=user_data["is_active"],
            is_superuser=user_data["is_superuser"],
            date_joined=user_data["date_joined"],
        )

        return user