from django.conf import settings
from django.db import models


# ============================================================
# FARM MODEL
# ============================================================
# Stores the basic information of a poultry farm.
# One User can own multiple Farms.
# ============================================================

class Farm(models.Model):
    FARM_TYPES = [
        ("BROILER", "Broiler"),
        ("LAYER", "Layer"),
        ("SONALI", "Sonali"),
        ("MIXED", "Mixed"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farms",
    )

    name = models.CharField(max_length=200)

    location = models.CharField(max_length=255)

    farm_type = models.CharField(
        max_length=10,
        choices=FARM_TYPES,
    )

    capacity = models.PositiveIntegerField()

    start_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_farm_name_per_owner",
            ),
        ]

    def __str__(self):
        return self.name




# ============================================================
# BATCH MODEL
# ============================================================
# Stores a group of poultry within a specific farm.
# One Farm can have multiple Batches.
# A Batch represents a group of birds started together.
# ============================================================

class Batch(models.Model):
    # Available poultry types for a batch
    POULTRY_TYPES = [
        ("BROILER", "Broiler"),
        ("LAYER", "Layer"),
        ("SONALI", "Sonali"),
        ("OTHER", "Other"),
    ]

    # Connects this Batch to a specific Farm.
    # One Farm can have many Batches.
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="batches",
    )

    # Unique batch identification within a Farm.
    # Example: B-001, B-002
    code = models.CharField(max_length=50)

    # Type of poultry in this batch.
    poultry_type = models.CharField(
        max_length=10,
        choices=POULTRY_TYPES,
    )

    # Date when the batch started.
    start_date = models.DateField()

    # Number of birds when the batch was initially started.
    initial_bird_count = models.PositiveIntegerField()

    # Purchase price of one bird.
    # DecimalField is used for accurate monetary values.
    purchase_price_per_bird = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    # Shows whether the batch is currently active.
    is_active = models.BooleanField(default=True)

    # Optional additional information.
    notes = models.TextField(blank=True)

    # Prevents duplicate batch codes within the same Farm.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["farm", "code"],
                name="unique_batch_code_per_farm",
            ),
        ]

    def __str__(self):
        return self.code


# ============================================================
# DAILY RECORD MODEL
# ============================================================
# Stores the daily status and activities of a poultry batch.
# One Batch can have many DailyRecords.

# ============================================================

class DailyRecord(models.Model):

    # Connects the daily record to a specific Batch.
    # One Batch can have many DailyRecords.
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="daily_records",
    )

    # Date of this daily record.
    record_date = models.DateField()

    # Amount of feed used on this day.
    feed_amount_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Amount of water used on this day.
    water_liters = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Number of birds that died on this day.
    dead_count = models.PositiveIntegerField(default=0)

    # Number of sick birds on this day.
    sick_count = models.PositiveIntegerField(default=0)

    # Whether medicine was used on this day.
    medicine_used = models.BooleanField(default=False)

    # Amount of medicine used.
    medicine_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    # Optional additional information.
    notes = models.TextField(blank=True)

    # Prevents duplicate daily records for the same Batch and date.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "record_date"],
                name="unique_daily_record_per_batch_date",
            ),
        ]

    def __str__(self):
        return f"{self.batch.code} - {self.record_date}"


# ============================================================
# EGG PRODUCTION MODEL
# ============================================================
# Stores daily egg production information for a poultry batch.
# One Batch can have many EggProduction records.
# ============================================================

class EggProduction(models.Model):

    # Connects egg production to a specific Batch.
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="egg_productions",
    )

    # Date of egg production.
    production_date = models.DateField()

    # Total number of eggs produced.
    egg_count = models.PositiveIntegerField()

    # Number of damaged eggs.
    damaged_egg_count = models.PositiveIntegerField(default=0)

    # Optional additional information.
    notes = models.TextField(blank=True)

    # Prevents duplicate egg production records
    # for the same Batch and date.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["batch", "production_date"],
                name="unique_egg_production_per_batch_date",
            ),
        ]

    def __str__(self):
        return f"{self.batch.code} - {self.production_date}"



    # ============================================================
# EXPENSE MODEL
# ============================================================
# Stores expenses related to a Farm or a specific Batch.
#
# Expense can be:
# 1. FARM  → General farm expense
# 2. BATCH → Expense directly related to a specific batch
#
# Farm can have many Expenses.
# A Batch can have many Expenses.
# ============================================================

class Expense(models.Model):

    # Types of expenses
    EXPENSE_TYPES = [
        ("FARM", "Farm"),
        ("BATCH", "Batch"),
    ]

    # Connects the expense to a specific Farm.
    # One Farm can have many Expenses.
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="expenses",
    )

    # Optional connection to a specific Batch.
    # For FARM expense → this can be empty.
    # For BATCH expense → this should contain a Batch.
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="expenses",
        blank=True,
        null=True,
    )

    # Defines whether this is a Farm-level or Batch-level expense.
    expense_type = models.CharField(
        max_length=5,
        choices=EXPENSE_TYPES,
    )

    # Expense category.
    # Examples:
    # Feed, Medicine, Electricity, Labor, Equipment
    category = models.CharField(max_length=100)

    # Amount of money spent.
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    # Date when the expense occurred.
    expense_date = models.DateField()

    # Optional description.
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"


# ============================================================
# SALE MODEL
# ============================================================
# Stores sales made from a poultry farm.
#
# A Sale can represent:
# 1. Poultry/Bird sale
# 2. Egg sale
#
# One Farm can have many Sales.
# One Batch can have many Sales.
# ============================================================

class Sale(models.Model):

    # Types of sales
    SALE_TYPES = [
        ("POULTRY", "Poultry"),
        ("EGG", "Egg"),
    ]

    # Unit used for the sale.
    SALE_UNITS = [
        ("BIRD", "Bird"),
        ("EGG", "Egg"),
    ]

    # Connects the sale to a specific Farm.
    # One Farm can have many Sales.
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    # Connects the sale to the Batch.
    # A poultry or egg sale should come from a specific Batch.
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name="sales",
    )

    # Type of product being sold.
    sale_type = models.CharField(
        max_length=10,
        choices=SALE_TYPES,
    )

    # Unit of the quantity.
    unit = models.CharField(
        max_length=5,
        choices=SALE_UNITS,
    )

    # Quantity sold.
    quantity = models.PositiveIntegerField()

    # Price per unit.
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    # Date of sale.
    sale_date = models.DateField()

    # Optional buyer information.
    buyer_name = models.CharField(
        max_length=200,
        blank=True,
    )

    # Optional additional information.
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.sale_type} - {self.quantity}"