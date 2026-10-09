from django.db import connection


# ============================================================
# GET ALL EGG PRODUCTION RECORDS
# ============================================================

def get_egg_productions_by_owner(owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                ep.id,
                ep.batch_id,
                ep.production_date,
                ep.egg_count,
                ep.damaged_egg_count,
                ep.notes,
                b.code AS batch_code,
                f.name AS farm_name
            FROM poultry_eggproduction ep
            INNER JOIN poultry_batch b
                ON ep.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE f.owner_id = %s
            ORDER BY ep.production_date DESC, ep.id DESC
            """,
            [owner_id],
        )

        columns = [column[0] for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET SINGLE EGG PRODUCTION RECORD
# ============================================================

def get_egg_production_by_id(
    egg_production_id,
    owner_id,
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                ep.id,
                ep.batch_id,
                ep.production_date,
                ep.egg_count,
                ep.damaged_egg_count,
                ep.notes,
                b.code AS batch_code,
                f.name AS farm_name
            FROM poultry_eggproduction ep
            INNER JOIN poultry_batch b
                ON ep.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE ep.id = %s
              AND f.owner_id = %s
            """,
            [
                egg_production_id,
                owner_id,
            ],
        )

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))


# ============================================================
# GET BATCHES FOR EGG PRODUCTION
# ============================================================

def get_batches_for_egg_production(owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                b.id,
                b.code AS batch_code,
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
# CREATE EGG PRODUCTION
# ============================================================

def create_egg_production(
    owner_id,
    batch_id,
    production_date,
    egg_count,
    damaged_egg_count,
    notes,
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO poultry_eggproduction (
                batch_id,
                production_date,
                egg_count,
                damaged_egg_count,
                notes
            )
            SELECT
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
                batch_id,
                production_date,
                egg_count,
                damaged_egg_count,
                notes,
                batch_id,
                owner_id,
            ],
        )


# ============================================================
# UPDATE EGG PRODUCTION
# ============================================================

def update_egg_production(
    egg_production_id,
    owner_id,
    batch_id,
    production_date,
    egg_count,
    damaged_egg_count,
    notes,
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            UPDATE poultry_eggproduction ep
            INNER JOIN poultry_batch b
                ON ep.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            SET
                ep.batch_id = %s,
                ep.production_date = %s,
                ep.egg_count = %s,
                ep.damaged_egg_count = %s,
                ep.notes = %s
            WHERE ep.id = %s
              AND f.owner_id = %s
            """,
            [
                batch_id,
                production_date,
                egg_count,
                damaged_egg_count,
                notes,
                egg_production_id,
                owner_id,
            ],
        )


# ============================================================
# DELETE EGG PRODUCTION
# ============================================================

def delete_egg_production(
    egg_production_id,
    owner_id,
):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            DELETE ep
            FROM poultry_eggproduction ep
            INNER JOIN poultry_batch b
                ON ep.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE ep.id = %s
              AND f.owner_id = %s
            """,
            [
                egg_production_id,
                owner_id,
            ],
        )




        # ============================================================
# GET TOTAL EGG PRODUCTION
# ============================================================

def get_total_egg_production_by_owner(owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(ep.egg_count), 0) AS total_egg_production
            FROM poultry_eggproduction ep
            INNER JOIN poultry_batch b
                ON ep.batch_id = b.id
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE f.owner_id = %s
            """,
            [owner_id],
        )

        row = cursor.fetchone()

        return row[0] if row else 0