from django.db import connection


def get_farms_by_owner(owner_id):
    """
    Return all farms belonging to a specific user.
    """

    sql = """
        SELECT
            id,
            name,
            location,
            farm_type,
            capacity,
            start_date,
            created_at
        FROM poultry_farm
        WHERE owner_id = %s
        ORDER BY id DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [owner_id])
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

    return [dict(zip(columns, row)) for row in rows]


def get_farm_by_id(farm_id, owner_id):
    """
    Return one farm only if it belongs to the specified user.
    """

    sql = """
        SELECT
            id,
            name,
            location,
            farm_type,
            capacity,
            start_date,
            created_at
        FROM poultry_farm
        WHERE id = %s
          AND owner_id = %s
        LIMIT 1;
    """

    with connection.cursor() as cursor:
        cursor.execute(sql, [farm_id, owner_id])
        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]

    return dict(zip(columns, row))


def create_farm(
    owner_id,
    name,
    location,
    farm_type,
    capacity,
    start_date,
):
    """
    Create a new farm using Raw SQL.
    """

    sql = """
        INSERT INTO poultry_farm
        (
            owner_id,
            name,
            location,
            farm_type,
            capacity,
            start_date,
            created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, NOW());
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            [
                owner_id,
                name,
                location,
                farm_type,
                capacity,
                start_date,
            ],
        )

        return cursor.lastrowid


def update_farm(
    farm_id,
    owner_id,
    name,
    location,
    farm_type,
    capacity,
    start_date,
):
    """
    Update a farm only if it belongs to the specified user.
    """

    sql = """
        UPDATE poultry_farm
        SET
            name = %s,
            location = %s,
            farm_type = %s,
            capacity = %s,
            start_date = %s
        WHERE id = %s
          AND owner_id = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            [
                name,
                location,
                farm_type,
                capacity,
                start_date,
                farm_id,
                owner_id,
            ],
        )

        return cursor.rowcount


def delete_farm(farm_id, owner_id):
    """
    Delete a farm only if it belongs to the specified user.
    """

    sql = """
        DELETE FROM poultry_farm
        WHERE id = %s
          AND owner_id = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(
            sql,
            [
                farm_id,
                owner_id,
            ],
        )

        return cursor.rowcount