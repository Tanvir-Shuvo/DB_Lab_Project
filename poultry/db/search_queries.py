from django.db import connection


# ============================================================
# GLOBAL SEARCH
# ============================================================

def global_search(owner_id, keyword):
    """
    Search all major poultry management modules
    for records belonging to the logged-in user.
    """

    keyword = keyword.strip()

    if not keyword:
        return {
            "farms": [],
            "batches": [],
            "daily_records": [],
            "egg_productions": [],
            "expenses": [],
            "sales": [],
        }

    search = f"%{keyword}%"

    # ========================================================
    # FARMS
    # ========================================================

    farm_sql = """
        SELECT
            id,
            name,
            location,
            farm_type,
            capacity,
            start_date
        FROM poultry_farm
        WHERE owner_id = %s
          AND (
                name LIKE %s
                OR location LIKE %s
                OR farm_type LIKE %s
          )
        ORDER BY id DESC;
    """

    # ========================================================
    # BATCHES
    # ========================================================

    batch_sql = """
        SELECT
            b.id,
            b.code,
            b.poultry_type,
            b.start_date,
            b.initial_bird_count,
            b.purchase_price_per_bird,
            b.is_active,
            f.name AS farm_name
        FROM poultry_batch b
        INNER JOIN poultry_farm f
            ON b.farm_id = f.id
        WHERE f.owner_id = %s
          AND (
                b.code LIKE %s
                OR b.poultry_type LIKE %s
                OR f.name LIKE %s
          )
        ORDER BY b.id DESC;
    """

    # ========================================================
    # DAILY RECORDS
    # ========================================================

    daily_record_sql = """
        SELECT
            dr.id,
            dr.record_date,
            dr.feed_amount_kg,
            dr.water_liters,
            dr.dead_birds,
            dr.sick_birds,
            dr.medicine,
            dr.notes,
            b.code AS batch_code,
            f.name AS farm_name
        FROM poultry_dailyrecord dr
        INNER JOIN poultry_batch b
            ON dr.batch_id = b.id
        INNER JOIN poultry_farm f
            ON b.farm_id = f.id
        WHERE f.owner_id = %s
          AND (
                b.code LIKE %s
                OR f.name LIKE %s
                OR dr.medicine LIKE %s
                OR dr.notes LIKE %s
          )
        ORDER BY dr.id DESC;
    """

    # ========================================================
    # EGG PRODUCTION
    # ========================================================

    egg_sql = """
        SELECT
            ep.id,
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
          AND (
                b.code LIKE %s
                OR f.name LIKE %s
                OR ep.notes LIKE %s
          )
        ORDER BY ep.id DESC;
    """

    # ========================================================
    # EXPENSES
    # ========================================================

    expense_sql = """
        SELECT
            e.id,
            e.expense_type,
            e.amount,
            e.expense_date,
            e.description,
            f.name AS farm_name,
            b.code AS batch_code
        FROM poultry_expense e
        LEFT JOIN poultry_farm f
            ON e.farm_id = f.id
        LEFT JOIN poultry_batch b
            ON e.batch_id = b.id
        WHERE e.owner_id = %s
          AND (
                e.expense_type LIKE %s
                OR e.description LIKE %s
                OR f.name LIKE %s
                OR b.code LIKE %s
          )
        ORDER BY e.id DESC;
    """

    # ========================================================
    # SALES
    # ========================================================

    sale_sql = """
        SELECT
            s.id,
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
        LEFT JOIN poultry_farm f
            ON s.farm_id = f.id
        LEFT JOIN poultry_batch b
            ON s.batch_id = b.id
        WHERE s.owner_id = %s
          AND (
                s.sale_type LIKE %s
                OR s.unit LIKE %s
                OR s.buyer_name LIKE %s
                OR s.notes LIKE %s
                OR f.name LIKE %s
                OR b.code LIKE %s
          )
        ORDER BY s.id DESC;
    """

    results = {}

    # ========================================================
    # EXECUTE FARM SEARCH
    # ========================================================

    with connection.cursor() as cursor:

        cursor.execute(
            farm_sql,
            [
                owner_id,
                search,
                search,
                search,
            ],
        )

        rows = cursor.fetchall()
        columns = [
            column[0]
            for column in cursor.description
        ]

        results["farms"] = [
            dict(zip(columns, row))
            for row in rows
        ]

    # ========================================================
    # EXECUTE BATCH SEARCH
    # ========================================================

    with connection.cursor() as cursor:

        cursor.execute(
            batch_sql,
            [
                owner_id,
                search,
                search,
                search,
            ],
        )

        rows = cursor.fetchall()
        columns = [
            column[0]
            for column in cursor.description
        ]

        results["batches"] = [
            dict(zip(columns, row))
            for row in rows
        ]

    # ========================================================
    # EXECUTE DAILY RECORD SEARCH
    # ========================================================

    with connection.cursor() as cursor:

        cursor.execute(
            daily_record_sql,
            [
                owner_id,
                search,
                search,
                search,
                search,
            ],
        )

        rows = cursor.fetchall()
        columns = [
            column[0]
            for column in cursor.description
        ]

        results["daily_records"] = [
            dict(zip(columns, row))
            for row in rows
        ]

    # ========================================================
    # EXECUTE EGG PRODUCTION SEARCH
    # ========================================================

    with connection.cursor() as cursor:

        cursor.execute(
            egg_sql,
            [
                owner_id,
                search,
                search,
                search,
            ],
        )

        rows = cursor.fetchall()
        columns = [
            column[0]
            for column in cursor.description
        ]

        results["egg_productions"] = [
            dict(zip(columns, row))
            for row in rows
        ]

    # ========================================================
    # EXECUTE EXPENSE SEARCH
    # ========================================================

    with connection.cursor() as cursor:

        cursor.execute(
            expense_sql,
            [
                owner_id,
                search,
                search,
                search,
                search,
            ],
        )

        rows = cursor.fetchall()
        columns = [
            column[0]
            for column in cursor.description
        ]

        results["expenses"] = [
            dict(zip(columns, row))
            for row in rows
        ]

    # ========================================================
    # EXECUTE SALE SEARCH
    # ========================================================

    with connection.cursor() as cursor:

        cursor.execute(
            sale_sql,
            [
                owner_id,
                search,
                search,
                search,
                search,
                search,
                search,
            ],
        )

        rows = cursor.fetchall()
        columns = [
            column[0]
            for column in cursor.description
        ]

        results["sales"] = [
            dict(zip(columns, row))
            for row in rows
        ]

    return results