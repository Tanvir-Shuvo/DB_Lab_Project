from django.contrib.auth.hashers import make_password
from django.db import connection


def create_user(username, email, password):
    password_hash = make_password(password)

    sql = """
        INSERT INTO auth_user
        (
            username,
            first_name,
            last_name,
            email,
            password,
            is_staff,
            is_active,
            is_superuser,
            date_joined
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW());
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            [
                username,
                "",
                "",
                email,
                password_hash,
                0,
                1,
                0,
            ],
        )


def get_user_by_username(username):
    """
    Fetch a user by username using Raw SQL.
    """

    sql = """
        SELECT
            id,
            username,
            first_name,
            last_name,
            email,
            password,
            is_staff,
            is_active,
            is_superuser,
            date_joined
        FROM auth_user
        WHERE username = %s
        LIMIT 1;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [username])
        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]

    return dict(zip(columns, row))


def get_user_by_id(user_id):
    """
    Fetch a user by primary key using Raw SQL.
    """

    sql = """
        SELECT
            id,
            username,
            first_name,
            last_name,
            email,
            password,
            is_staff,
            is_active,
            is_superuser,
            date_joined
        FROM auth_user
        WHERE id = %s
        LIMIT 1;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [user_id])
        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]

    return dict(zip(columns, row))