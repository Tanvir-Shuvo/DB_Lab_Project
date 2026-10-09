from django.contrib import admin

from .models import (
    Farm,
    Batch,
    DailyRecord,
    EggProduction,
    Expense,
    Sale,
)


# ============================================================
# FARM ADMIN
# ============================================================

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "location",
        "farm_type",
        "capacity",
        "start_date",
    )

    list_filter = (
    "farm_type",
    )

    search_fields = (
        "name",
        "location",
        "owner__username",
    )


# ============================================================
# BATCH ADMIN
# ============================================================

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "farm",
        "poultry_type",
        "start_date",
        "initial_bird_count",
        "purchase_price_per_bird",
        "is_active",
    )

    list_filter = (
        "poultry_type",
        "is_active",
    )

    search_fields = (
        "code",
        "farm__name",
    )


# ============================================================
# DAILY RECORD ADMIN
# ============================================================

@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "batch",
        "record_date",
        "feed_amount_kg",
        "water_liters",
        "dead_count",
        "sick_count",
        "medicine_used",
    )

    list_filter = (
        "medicine_used",
        "record_date",
    )

    search_fields = (
        "batch__code",
        "batch__farm__name",
    )


# ============================================================
# EGG PRODUCTION ADMIN
# ============================================================

@admin.register(EggProduction)
class EggProductionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "batch",
        "production_date",
        "egg_count",
        "damaged_egg_count",
    )

    list_filter = (
        "production_date",
    )

    search_fields = (
        "batch__code",
        "batch__farm__name",
    )


# ============================================================
# EXPENSE ADMIN
# ============================================================

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "farm",
        "batch",
        "expense_type",
        "category",
        "amount",
        "expense_date",
    )

    list_filter = (
        "expense_type",
        "expense_date",
    )

    search_fields = (
        "category",
        "farm__name",
        "batch__code",
    )


# ============================================================
# SALE ADMIN
# ============================================================

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "farm",
        "batch",
        "sale_type",
        "unit",
        "quantity",
        "unit_price",
        "sale_date",
        "buyer_name",
    )

    list_filter = (
        "sale_type",
        "unit",
        "sale_date",
    )

    search_fields = (
        "farm__name",
        "batch__code",
        "buyer_name",
    )