from django.db import connection


# ============================================================
# EXPENSE LIST
# ============================================================

def get_expenses_by_owner(owner_id):
    """
    Get all expenses belonging to farms owned by the user.
    Uses Raw SQL only.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                e.id,
                e.farm_id,
                e.batch_id,
                e.expense_type,
                e.category,
                e.amount,
                e.expense_date,
                e.description,
                f.name AS farm_name,
                b.code AS batch_code
            FROM poultry_expense e
            INNER JOIN poultry_farm f
                ON e.farm_id = f.id
            LEFT JOIN poultry_batch b
                ON e.batch_id = b.id
            WHERE f.owner_id = %s
            ORDER BY e.expense_date DESC, e.id DESC
            """,
            [owner_id],
        )

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET SINGLE EXPENSE
# ============================================================

def get_expense_by_id(expense_id, owner_id):
    """
    Get one expense only if it belongs to the current user's farm.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                e.id,
                e.farm_id,
                e.batch_id,
                e.expense_type,
                e.category,
                e.amount,
                e.expense_date,
                e.description,
                f.name AS farm_name,
                b.code AS batch_code
            FROM poultry_expense e
            INNER JOIN poultry_farm f
                ON e.farm_id = f.id
            LEFT JOIN poultry_batch b
                ON e.batch_id = b.id
            WHERE e.id = %s
              AND f.owner_id = %s
            LIMIT 1
            """,
            [expense_id, owner_id],
        )

        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))


# ============================================================
# GET USER'S FARMS
# ============================================================

def get_farms_for_expense(owner_id):
    """
    Get farms owned by the current user.
    Used in the Expense create/update form.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                id,
                name
            FROM poultry_farm
            WHERE owner_id = %s
            ORDER BY name ASC
            """,
            [owner_id],
        )

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET USER'S BATCHES
# ============================================================

def get_batches_for_expense(owner_id):
    """
    Get batches belonging to farms owned by the current user.
    Used in the Expense create/update form.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                b.id,
                b.code,
                b.farm_id,
                f.name AS farm_name
            FROM poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE f.owner_id = %s
            ORDER BY f.name ASC, b.code ASC
            """,
            [owner_id],
        )

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# CREATE EXPENSE
# ============================================================

def create_expense(
    owner_id,
    farm_id,
    batch_id,
    expense_type,
    category,
    amount,
    expense_date,
    description,
):
    """
    Create an Expense only when the selected farm belongs
    to the current user.

    For BATCH expenses, the selected batch must also belong
    to the selected farm.
    """

    with connection.cursor() as cursor:

        if expense_type == "BATCH":
            cursor.execute(
                """
                INSERT INTO poultry_expense (
                    farm_id,
                    batch_id,
                    expense_type,
                    category,
                    amount,
                    expense_date,
                    description
                )
                SELECT
                    f.id,
                    b.id,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                FROM poultry_farm f
                INNER JOIN poultry_batch b
                    ON b.farm_id = f.id
                WHERE f.id = %s
                  AND b.id = %s
                  AND f.owner_id = %s
                """,
                [
                    expense_type,
                    category,
                    amount,
                    expense_date,
                    description,
                    farm_id,
                    batch_id,
                    owner_id,
                ],
            )

        else:
            cursor.execute(
                """
                INSERT INTO poultry_expense (
                    farm_id,
                    batch_id,
                    expense_type,
                    category,
                    amount,
                    expense_date,
                    description
                )
                SELECT
                    f.id,
                    NULL,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                FROM poultry_farm f
                WHERE f.id = %s
                  AND f.owner_id = %s
                """,
                [
                    expense_type,
                    category,
                    amount,
                    expense_date,
                    description,
                    farm_id,
                    owner_id,
                ],
            )

        return cursor.rowcount > 0


# ============================================================
# UPDATE EXPENSE
# ============================================================

def update_expense(
    expense_id,
    owner_id,
    farm_id,
    batch_id,
    expense_type,
    category,
    amount,
    expense_date,
    description,
):
    """
    Update an Expense only if the existing expense and the
    selected farm/batch belong to the current user.
    """

    with connection.cursor() as cursor:

        if expense_type == "BATCH":
            cursor.execute(
                """
                UPDATE poultry_expense e
                INNER JOIN poultry_farm f
                    ON e.farm_id = f.id
                INNER JOIN poultry_batch b
                    ON b.farm_id = f.id
                SET
                    e.farm_id = f.id,
                    e.batch_id = b.id,
                    e.expense_type = %s,
                    e.category = %s,
                    e.amount = %s,
                    e.expense_date = %s,
                    e.description = %s
                WHERE e.id = %s
                  AND f.id = %s
                  AND b.id = %s
                  AND f.owner_id = %s
                """,
                [
                    expense_type,
                    category,
                    amount,
                    expense_date,
                    description,
                    expense_id,
                    farm_id,
                    batch_id,
                    owner_id,
                ],
            )

        else:
            cursor.execute(
                """
                UPDATE poultry_expense e
                INNER JOIN poultry_farm f
                    ON e.farm_id = f.id
                SET
                    e.farm_id = f.id,
                    e.batch_id = NULL,
                    e.expense_type = %s,
                    e.category = %s,
                    e.amount = %s,
                    e.expense_date = %s,
                    e.description = %s
                WHERE e.id = %s
                  AND f.id = %s
                  AND f.owner_id = %s
                """,
                [
                    expense_type,
                    category,
                    amount,
                    expense_date,
                    description,
                    expense_id,
                    farm_id,
                    owner_id,
                ],
            )

        return cursor.rowcount > 0


# ============================================================
# DELETE EXPENSE
# ============================================================

def delete_expense(expense_id, owner_id):
    """
    Delete an Expense only if it belongs to the
    current user's farm.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE e
            FROM poultry_expense e
            INNER JOIN poultry_farm f
                ON e.farm_id = f.id
            WHERE e.id = %s
              AND f.owner_id = %s
            """,
            [expense_id, owner_id],
        )

        return cursor.rowcount > 0