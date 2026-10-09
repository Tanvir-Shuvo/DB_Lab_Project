from django.db import connection


# ============================================================
# DAILY RECORD LIST
# ============================================================

def get_records_by_owner(owner_id):
    """
    Get all daily records belonging to farms owned by the user.
    Uses Raw SQL only.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                r.id,
                r.batch_id,
                r.record_date,
                r.feed_amount_kg,
                r.water_liters,
                r.dead_count,
                r.sick_count,
                r.medicine_used,
                r.medicine_quantity,
                r.notes,
                b.code AS batch_code,
                f.name AS farm_name
            FROM poultry_dailyrecord r
            INNER JOIN poultry_batch b
                ON r.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE f.owner_id = %s
            ORDER BY r.record_date DESC, r.id DESC
            """,
            [owner_id],
        )

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET SINGLE DAILY RECORD
# ============================================================

def get_record_by_id(record_id, owner_id):
    """
    Get one daily record only if it belongs to the current user.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                r.id,
                r.batch_id,
                r.record_date,
                r.feed_amount_kg,
                r.water_liters,
                r.dead_count,
                r.sick_count,
                r.medicine_used,
                r.medicine_quantity,
                r.notes,
                b.code AS batch_code,
                f.name AS farm_name
            FROM poultry_dailyrecord r
            INNER JOIN poultry_batch b
                ON r.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE r.id = %s
              AND f.owner_id = %s
            LIMIT 1
            """,
            [record_id, owner_id],
        )

        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))


# ============================================================
# GET USER'S BATCHES
# ============================================================

def get_batches_for_record(owner_id):
    """
    Get batches owned by the current user.
    Used in the Daily Record create/update form.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                b.id,
                b.code,
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
# CREATE DAILY RECORD
# ============================================================

def create_record(
    owner_id,
    batch_id,
    record_date,
    feed_amount_kg,
    water_liters,
    dead_count,
    sick_count,
    medicine_used,
    medicine_quantity,
    notes,
):
    """
    Create a Daily Record only when the selected batch
    belongs to the current user's farm.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO poultry_dailyrecord (
                batch_id,
                record_date,
                feed_amount_kg,
                water_liters,
                dead_count,
                sick_count,
                medicine_used,
                medicine_quantity,
                notes
            )
            SELECT
                b.id,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            FROM poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE b.id = %s
              AND f.owner_id = %s
            """,
            [
                record_date,
                feed_amount_kg,
                water_liters,
                dead_count,
                sick_count,
                medicine_used,
                medicine_quantity,
                notes,
                batch_id,
                owner_id,
            ],
        )

        return cursor.rowcount > 0


# ============================================================
# UPDATE DAILY RECORD
# ============================================================

def update_record(
    record_id,
    owner_id,
    batch_id,
    record_date,
    feed_amount_kg,
    water_liters,
    dead_count,
    sick_count,
    medicine_used,
    medicine_quantity,
    notes,
):
    """
    Update a Daily Record only if the record and the
    selected batch belong to the current user's farm.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE poultry_dailyrecord r
            INNER JOIN poultry_batch b
                ON r.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            SET
                r.batch_id = %s,
                r.record_date = %s,
                r.feed_amount_kg = %s,
                r.water_liters = %s,
                r.dead_count = %s,
                r.sick_count = %s,
                r.medicine_used = %s,
                r.medicine_quantity = %s,
                r.notes = %s
            WHERE r.id = %s
              AND f.owner_id = %s
            """,
            [
                batch_id,
                record_date,
                feed_amount_kg,
                water_liters,
                dead_count,
                sick_count,
                medicine_used,
                medicine_quantity,
                notes,
                record_id,
                owner_id,
            ],
        )

        return cursor.rowcount > 0


# ============================================================
# DELETE DAILY RECORD
# ============================================================

def delete_record(record_id, owner_id):
    """
    Delete a Daily Record only if it belongs to the
    current user's farm.
    """

    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE r
            FROM poultry_dailyrecord r
            INNER JOIN poultry_batch b
                ON r.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE r.id = %s
              AND f.owner_id = %s
            """,
            [record_id, owner_id],
        )

        return cursor.rowcount > 0