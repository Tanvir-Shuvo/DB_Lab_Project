
from django.db import connection


# ============================================================
# GET ALL SALES FOR CURRENT USER
# ============================================================

def get_sales_by_owner(owner_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                s.id,
                s.farm_id,
                s.batch_id,
                s.sale_type,
                s.unit,
                s.quantity,
                s.unit_price,
                s.sale_date,
                s.buyer_name,
                s.notes,
                f.name AS farm_name,
                b.code AS batch_code
            FROM poultry_sale s
            INNER JOIN poultry_farm f
                ON s.farm_id = f.id
            INNER JOIN poultry_batch b
                ON s.batch_id = b.id
            WHERE f.owner_id = %s
            ORDER BY s.sale_date DESC, s.id DESC
            """,
            [owner_id],
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET SINGLE SALE
# ============================================================

def get_sale_by_id(sale_id, owner_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                s.id,
                s.farm_id,
                s.batch_id,
                s.sale_type,
                s.unit,
                s.quantity,
                s.unit_price,
                s.sale_date,
                s.buyer_name,
                s.notes,
                f.name AS farm_name,
                b.code AS batch_code
            FROM poultry_sale s
            INNER JOIN poultry_farm f
                ON s.farm_id = f.id
            INNER JOIN poultry_batch b
                ON s.batch_id = b.id
            WHERE s.id = %s
              AND f.owner_id = %s
            LIMIT 1
            """,
            [
                sale_id,
                owner_id,
            ],
        )

        row = cursor.fetchone()

        if row is None:
            return None

        columns = [
            column[0]
            for column in cursor.description
        ]

        return dict(
            zip(
                columns,
                row,
            )
        )


# ============================================================
# GET FARMS FOR SALE FORM
# ============================================================

def get_farms_for_sale(owner_id):
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

        columns = [
            column[0]
            for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# GET BATCHES FOR SALE FORM
# ============================================================

def get_batches_for_sale(owner_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                b.id,
                b.farm_id,
                b.code,
                b.poultry_type,
                f.name AS farm_name
            FROM poultry_batch b
            INNER JOIN poultry_farm f
                ON b.farm_id = f.id
            WHERE f.owner_id = %s
            ORDER BY f.name ASC, b.code ASC
            """,
            [owner_id],
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


# ============================================================
# CREATE SALE
# ============================================================

def create_sale(
    owner_id,
    farm_id,
    batch_id,
    sale_type,
    unit,
    quantity,
    unit_price,
    sale_date,
    buyer_name,
    notes,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO poultry_sale (
                farm_id,
                batch_id,
                sale_type,
                unit,
                quantity,
                unit_price,
                sale_date,
                buyer_name,
                notes
            )
            SELECT
                f.id,
                b.id,
                %s,
                %s,
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
            LIMIT 1
            """,
            [
                sale_type,
                unit,
                quantity,
                unit_price,
                sale_date,
                buyer_name,
                notes,
                farm_id,
                batch_id,
                owner_id,
            ],
        )


# ============================================================
# UPDATE SALE
# ============================================================

def update_sale(
    sale_id,
    owner_id,
    farm_id,
    batch_id,
    sale_type,
    unit,
    quantity,
    unit_price,
    sale_date,
    buyer_name,
    notes,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE poultry_sale s
            INNER JOIN poultry_farm f
                ON s.farm_id = f.id
            INNER JOIN poultry_batch b
                ON b.farm_id = f.id
            SET
                s.farm_id = %s,
                s.batch_id = %s,
                s.sale_type = %s,
                s.unit = %s,
                s.quantity = %s,
                s.unit_price = %s,
                s.sale_date = %s,
                s.buyer_name = %s,
                s.notes = %s
            WHERE s.id = %s
              AND f.owner_id = %s
              AND b.id = %s
              AND b.farm_id = %s
            """,
            [
                farm_id,
                batch_id,
                sale_type,
                unit,
                quantity,
                unit_price,
                sale_date,
                buyer_name,
                notes,
                sale_id,
                owner_id,
                batch_id,
                farm_id,
            ],
        )


# ============================================================
# DELETE SALE
# ============================================================

def delete_sale(sale_id, owner_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE s
            FROM poultry_sale s
            INNER JOIN poultry_farm f
                ON s.farm_id = f.id
            WHERE s.id = %s
              AND f.owner_id = %s
            """,
            [
                sale_id,
                owner_id,
            ],
        )


# ============================================================
# GET TOTAL SALES
# ============================================================

def get_total_sales_by_owner(owner_id):

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                COALESCE(
                    SUM(s.quantity * s.unit_price),
                    0
                ) AS total_sales
            FROM poultry_sale s
            INNER JOIN poultry_farm f
                ON s.farm_id = f.id
            WHERE f.owner_id = %s
            """,
            [owner_id],
        )

        row = cursor.fetchone()

        return row[0] if row else 0