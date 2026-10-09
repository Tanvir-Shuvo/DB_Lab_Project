from django.db import connection


# ============================================================
# BATCH QUERIES
# ============================================================
# All Batch database operations are handled using Raw SQL.
# Batch ownership is verified through the related Farm owner.
# ============================================================


# ============================================================
# GET ALL BATCHES OF A USER
# ============================================================

def get_batches_by_owner(owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                b.id,
                b.farm_id,
                b.code,
                b.poultry_type,
                b.start_date,
                b.initial_bird_count,
                b.purchase_price_per_bird,
                b.is_active,
                b.notes,
                f.name AS farm_name
            FROM poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE f.owner_id = %s
            ORDER BY b.id DESC
            """,
            [owner_id],
        )

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET SINGLE BATCH
# ============================================================

def get_batch_by_id(batch_id, owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                b.id,
                b.farm_id,
                b.code,
                b.poultry_type,
                b.start_date,
                b.initial_bird_count,
                b.purchase_price_per_bird,
                b.is_active,
                b.notes,
                f.name AS farm_name
            FROM poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE b.id = %s
              AND f.owner_id = %s
            LIMIT 1
            """,
            [batch_id, owner_id],
        )

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))


# ============================================================
# GET FARMS OF A USER
# ============================================================
# Used in the Batch Create/Update form so that the user can
# select only their own farms.
# ============================================================

def get_farms_for_batch(owner_id):

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
# CREATE BATCH
# ============================================================

def create_batch(
    owner_id,
    farm_id,
    code,
    poultry_type,
    start_date,
    initial_bird_count,
    purchase_price_per_bird,
    is_active,
    notes,
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO poultry_batch (
                farm_id,
                code,
                poultry_type,
                start_date,
                initial_bird_count,
                purchase_price_per_bird,
                is_active,
                notes
            )
            SELECT
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            FROM poultry_farm
            WHERE id = %s
              AND owner_id = %s
            """,
            [
                farm_id,
                code,
                poultry_type,
                start_date,
                initial_bird_count,
                purchase_price_per_bird,
                is_active,
                notes,
                farm_id,
                owner_id,
            ],
        )

        return cursor.rowcount


# ============================================================
# UPDATE BATCH
# ============================================================

def update_batch(
    batch_id,
    owner_id,
    farm_id,
    code,
    poultry_type,
    start_date,
    initial_bird_count,
    purchase_price_per_bird,
    is_active,
    notes,
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            UPDATE poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            SET
                b.farm_id = %s,
                b.code = %s,
                b.poultry_type = %s,
                b.start_date = %s,
                b.initial_bird_count = %s,
                b.purchase_price_per_bird = %s,
                b.is_active = %s,
                b.notes = %s
            WHERE b.id = %s
              AND f.owner_id = %s
            """,
            [
                farm_id,
                code,
                poultry_type,
                start_date,
                initial_bird_count,
                purchase_price_per_bird,
                is_active,
                notes,
                batch_id,
                owner_id,
            ],
        )

        return cursor.rowcount


# ============================================================
# DELETE BATCH
# ============================================================

def delete_batch(batch_id, owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            DELETE b
            FROM poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE b.id = %s
              AND f.owner_id = %s
            """,
            [
                batch_id,
                owner_id,
            ],
        )

        return cursor.rowcount