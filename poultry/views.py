from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .db.user_queries import (
    create_user,
    get_user_by_username,
)

from .db.farm_queries import (
    get_farms_by_owner,
    get_farm_by_id,
    create_farm,
    update_farm,
    delete_farm,
)

from .db.batch_queries import (
    get_batches_by_owner,
    get_batch_by_id,
    get_farms_for_batch,
    create_batch,
    update_batch,
    delete_batch,
)

from .db.daily_record_queries import (
    get_records_by_owner,
    get_record_by_id,
    get_batches_for_record,
    create_record,
    update_record,
    delete_record,
)

from .db.egg_production_queries import (
    get_egg_productions_by_owner,
    get_egg_production_by_id,
    get_batches_for_egg_production,
    create_egg_production,
    update_egg_production,
    delete_egg_production,
    get_total_egg_production_by_owner,
)

from .db.expense_queries import (
    get_expenses_by_owner,
    get_expense_by_id,
    get_farms_for_expense,
    get_batches_for_expense,
    create_expense,
    update_expense,
    delete_expense,
)

from .db.sale_queries import (
    get_sales_by_owner,
    get_sale_by_id,
    get_farms_for_sale,
    get_batches_for_sale,
    create_sale,
    update_sale,
    delete_sale,
    get_total_sales_by_owner,
)

from .db.search_queries import (
    global_search,
)


# ============================================================
# HOME
# ============================================================

def home(request):

    return render(
        request,
        "home.html",
    )


# ============================================================
# REGISTER
# ============================================================

def register_view(request):

    if request.user.is_authenticated:

        return redirect(
            "dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        confirm_password = request.POST.get(
            "confirm_password",
            "",
        )

        if not username or not password:

            messages.error(
                request,
                "Username and password are required.",
            )

        elif password != confirm_password:

            messages.error(
                request,
                "Passwords do not match.",
            )

        elif get_user_by_username(username):

            messages.error(
                request,
                "Username already exists.",
            )

        else:

            try:

                create_user(
                    username=username,
                    password=password,
                )

                messages.success(
                    request,
                    "Registration successful. Please login.",
                )

                return redirect(
                    "login"
                )

            except IntegrityError:

                messages.error(
                    request,
                    "Username already exists.",
                )

    return render(
        request,
        "register.html",
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect(
            "dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            "",
        ).strip()

        password = request.POST.get(
            "password",
            "",
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(
                request,
                user,
            )

            return redirect(
                "dashboard"
            )

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "login.html",
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect(
        "login"
    )


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    owner_id = request.user.id

    farms = get_farms_by_owner(
        owner_id
    )

    batches = get_batches_by_owner(
        owner_id
    )

    daily_records = get_records_by_owner(
        owner_id
    )

    egg_productions = get_egg_productions_by_owner(
        owner_id
    )

    expenses = get_expenses_by_owner(
        owner_id
    )

    sales = get_sales_by_owner(
        owner_id
    )

    total_farms = len(farms)

    active_batches = sum(
        1
        for batch in batches
        if batch.get("is_active") == 1
        or batch.get("is_active") is True
    )

    total_egg_production = (
        get_total_egg_production_by_owner(
            owner_id
        )
    )

    total_sales = (
        get_total_sales_by_owner(
            owner_id
        )
    )

    context = {
        "username": request.user.username,
        "farms": farms,
        "batches": batches,
        "daily_records": daily_records,
        "egg_productions": egg_productions,
        "expenses": expenses,
        "sales": sales,
        "total_farms": total_farms,
        "active_batches": active_batches,
        "total_egg_production": total_egg_production,
        "total_sales": total_sales,
    }

    return render(
        request,
        "dashboard.html",
        context,
    )


# ============================================================
# GLOBAL SEARCH
# ============================================================

@login_required
def search_view(request):

    keyword = request.GET.get(
        "q",
        "",
    ).strip()

    results = {
        "farms": [],
        "batches": [],
        "daily_records": [],
        "egg_productions": [],
        "expenses": [],
        "sales": [],
    }

    if keyword:

        results = global_search(
            request.user.id,
            keyword,
        )

    total_results = sum(
        len(items)
        for items in results.values()
    )

    context = {
        "keyword": keyword,
        "results": results,
        "total_results": total_results,
    }

    return render(
        request,
        "search_results.html",
        context,
    )


# ============================================================
# FARM CRUD
# ============================================================

@login_required
def farm_list(request):

    owner_id = request.user.id

    farms = get_farms_by_owner(
        owner_id
    )

    return render(
        request,
        "farm_list.html",
        {
            "farms": farms,
        },
    )


@login_required
def farm_create(request):

    if request.method == "POST":

        owner_id = request.user.id

        name = request.POST.get(
            "name",
            "",
        ).strip()

        location = request.POST.get(
            "location",
            "",
        ).strip()

        farm_type = request.POST.get(
            "farm_type",
            "",
        ).strip()

        capacity = request.POST.get(
            "capacity",
            "",
        ).strip()

        start_date = request.POST.get(
            "start_date",
            "",
        ).strip()

        if not name:

            messages.error(
                request,
                "Farm name is required.",
            )

            return render(
                request,
                "farm_form.html",
            )

        try:

            create_farm(
                owner_id=owner_id,
                name=name,
                location=location,
                farm_type=farm_type,
                capacity=capacity,
                start_date=start_date,
            )

            messages.success(
                request,
                "Farm created successfully.",
            )

            return redirect(
                "farm_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "A farm with this name already exists.",
            )

    return render(
        request,
        "farm_form.html",
    )


@login_required
def farm_update(
    request,
    farm_id,
):

    owner_id = request.user.id

    farm = get_farm_by_id(
        farm_id=farm_id,
        owner_id=owner_id,
    )

    if farm is None:

        messages.error(
            request,
            "Farm not found.",
        )

        return redirect(
            "farm_list"
        )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            "",
        ).strip()

        location = request.POST.get(
            "location",
            "",
        ).strip()

        farm_type = request.POST.get(
            "farm_type",
            "",
        ).strip()

        capacity = request.POST.get(
            "capacity",
            "",
        ).strip()

        start_date = request.POST.get(
            "start_date",
            "",
        ).strip()

        if not name:

            messages.error(
                request,
                "Farm name is required.",
            )

            return render(
                request,
                "farm_form.html",
                {
                    "farm": farm,
                },
            )

        try:

            update_farm(
                farm_id=farm_id,
                owner_id=owner_id,
                name=name,
                location=location,
                farm_type=farm_type,
                capacity=capacity,
                start_date=start_date,
            )

            messages.success(
                request,
                "Farm updated successfully.",
            )

            return redirect(
                "farm_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "A farm with this name already exists.",
            )

    return render(
        request,
        "farm_form.html",
        {
            "farm": farm,
        },
    )


@login_required
def farm_delete(
    request,
    farm_id,
):

    owner_id = request.user.id

    farm = get_farm_by_id(
        farm_id=farm_id,
        owner_id=owner_id,
    )

    if farm is None:

        messages.error(
            request,
            "Farm not found.",
        )

        return redirect(
            "farm_list"
        )

    if request.method == "POST":

        try:

            delete_farm(
                farm_id=farm_id,
                owner_id=owner_id,
            )

            messages.success(
                request,
                "Farm deleted successfully.",
            )

            return redirect(
                "farm_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "This farm cannot be deleted because it has existing batches or related records. Please delete the related batches first.",
            )

            return redirect(
                "farm_list"
            )

    return render(
        request,
        "farm_confirm_delete.html",
        {
            "farm": farm,
        },
    )


# ============================================================
# BATCH CRUD
# ============================================================

@login_required
def batch_list(request):

    owner_id = request.user.id

    batches = get_batches_by_owner(
        owner_id
    )

    return render(
        request,
        "batch_list.html",
        {
            "batches": batches,
        },
    )


@login_required
def batch_create(request):

    owner_id = request.user.id

    farms = get_farms_for_batch(
        owner_id
    )

    if request.method == "POST":

        farm_id = request.POST.get(
            "farm_id",
            "",
        ).strip()

        code = request.POST.get(
            "code",
            "",
        ).strip()

        poultry_type = request.POST.get(
            "poultry_type",
            "",
        ).strip()

        start_date = request.POST.get(
            "start_date",
            "",
        ).strip()

        initial_bird_count = request.POST.get(
            "initial_bird_count",
            "",
        ).strip()

        purchase_price_per_bird = request.POST.get(
            "purchase_price_per_bird",
            "",
        ).strip()

        is_active = (
            request.POST.get(
                "is_active"
            ) == "on"
        )

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            create_batch(
                owner_id=owner_id,
                farm_id=farm_id,
                code=code,
                poultry_type=poultry_type,
                start_date=start_date,
                initial_bird_count=initial_bird_count,
                purchase_price_per_bird=purchase_price_per_bird,
                is_active=is_active,
                notes=notes,
            )

            messages.success(
                request,
                "Batch created successfully.",
            )

            return redirect(
                "batch_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "Batch code already exists for this farm.",
            )

    return render(
        request,
        "batch_form.html",
        {
            "farms": farms,
        },
    )


@login_required
def batch_update(
    request,
    batch_id,
):

    owner_id = request.user.id

    batch = get_batch_by_id(
        batch_id=batch_id,
        owner_id=owner_id,
    )

    farms = get_farms_for_batch(
        owner_id
    )

    if batch is None:

        messages.error(
            request,
            "Batch not found.",
        )

        return redirect(
            "batch_list"
        )

    if request.method == "POST":

        farm_id = request.POST.get(
            "farm_id",
            "",
        ).strip()

        code = request.POST.get(
            "code",
            "",
        ).strip()

        poultry_type = request.POST.get(
            "poultry_type",
            "",
        ).strip()

        start_date = request.POST.get(
            "start_date",
            "",
        ).strip()

        initial_bird_count = request.POST.get(
            "initial_bird_count",
            "",
        ).strip()

        purchase_price_per_bird = request.POST.get(
            "purchase_price_per_bird",
            "",
        ).strip()

        is_active = (
            request.POST.get(
                "is_active"
            ) == "on"
        )

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            update_batch(
                batch_id=batch_id,
                owner_id=owner_id,
                farm_id=farm_id,
                code=code,
                poultry_type=poultry_type,
                start_date=start_date,
                initial_bird_count=initial_bird_count,
                purchase_price_per_bird=purchase_price_per_bird,
                is_active=is_active,
                notes=notes,
            )

            messages.success(
                request,
                "Batch updated successfully.",
            )

            return redirect(
                "batch_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "Batch code already exists for this farm.",
            )

    return render(
        request,
        "batch_form.html",
        {
            "batch": batch,
            "farms": farms,
        },
    )


@login_required
def batch_delete(
    request,
    batch_id,
):

    owner_id = request.user.id

    batch = get_batch_by_id(
        batch_id=batch_id,
        owner_id=owner_id,
    )

    if batch is None:

        messages.error(
            request,
            "Batch not found.",
        )

        return redirect(
            "batch_list"
        )

    if request.method == "POST":

        delete_batch(
            batch_id=batch_id,
            owner_id=owner_id,
        )

        messages.success(
            request,
            "Batch deleted successfully.",
        )

        return redirect(
            "batch_list"
        )

    return render(
        request,
        "batch_confirm_delete.html",
        {
            "batch": batch,
        },
    )


# ============================================================
# DAILY RECORD CRUD
# ============================================================

@login_required
def daily_record_list(request):

    owner_id = request.user.id

    records = get_records_by_owner(
        owner_id
    )

    return render(
        request,
        "daily_record_list.html",
        {
            "records": records,
        },
    )


@login_required
def daily_record_create(request):

    owner_id = request.user.id

    batches = get_batches_for_record(
        owner_id
    )

    if request.method == "POST":

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        record_date = request.POST.get(
            "record_date",
            "",
        ).strip()

        feed_amount_kg = request.POST.get(
            "feed_amount_kg",
            "",
        ).strip()

        water_liters = request.POST.get(
            "water_liters",
            "",
        ).strip()

        dead_count = request.POST.get(
            "dead_count",
            "",
        ).strip()

        sick_count = request.POST.get(
            "sick_count",
            "",
        ).strip()

        medicine_used = 1 if request.POST.get(
            "medicine_used"
        ) == "on" else 0

        medicine_quantity = request.POST.get(
            "medicine_quantity",
            "",
        ).strip()

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            create_record(
                owner_id=owner_id,
                batch_id=batch_id,
                record_date=record_date,
                feed_amount_kg=feed_amount_kg,
                water_liters=water_liters,
                dead_count=dead_count,
                sick_count=sick_count,
                medicine_used=medicine_used,
                medicine_quantity=medicine_quantity,
                notes=notes,
            )

            messages.success(
                request,
                "Daily record created successfully.",
            )

            return redirect(
                "daily_record_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "A daily record already exists for this batch and date.",
            )

    return render(
        request,
        "daily_record_form.html",
        {
            "batches": batches,
        },
    )


@login_required
def daily_record_update(
    request,
    record_id,
):

    owner_id = request.user.id

    record = get_record_by_id(
        record_id=record_id,
        owner_id=owner_id,
    )

    batches = get_batches_for_record(
        owner_id
    )

    if record is None:

        messages.error(
            request,
            "Daily record not found.",
        )

        return redirect(
            "daily_record_list"
        )

    if request.method == "POST":

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        record_date = request.POST.get(
            "record_date",
            "",
        ).strip()

        feed_amount_kg = request.POST.get(
            "feed_amount_kg",
            "",
        ).strip()

        water_liters = request.POST.get(
            "water_liters",
            "",
        ).strip()

        dead_count = request.POST.get(
            "dead_count",
            "",
        ).strip()

        sick_count = request.POST.get(
            "sick_count",
            "",
        ).strip()

        medicine_used = 1 if request.POST.get(
            "medicine_used"
        ) == "on" else 0

        medicine_quantity = request.POST.get(
            "medicine_quantity",
            "",
        ).strip()

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            update_record(
                record_id=record_id,
                owner_id=owner_id,
                batch_id=batch_id,
                record_date=record_date,
                feed_amount_kg=feed_amount_kg,
                water_liters=water_liters,
                dead_count=dead_count,
                sick_count=sick_count,
                medicine_used=medicine_used,
                medicine_quantity=medicine_quantity,
                notes=notes,
            )

            messages.success(
                request,
                "Daily record updated successfully.",
            )

            return redirect(
                "daily_record_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "A daily record already exists for this batch and date.",
            )

    return render(
        request,
        "daily_record_form.html",
        {
            "record": record,
            "batches": batches,
        },
    )


@login_required
def daily_record_delete(
    request,
    record_id,
):

    owner_id = request.user.id

    record = get_record_by_id(
        record_id=record_id,
        owner_id=owner_id,
    )

    if record is None:

        messages.error(
            request,
            "Daily record not found.",
        )

        return redirect(
            "daily_record_list"
        )

    if request.method == "POST":

        delete_record(
            record_id=record_id,
            owner_id=owner_id,
        )

        messages.success(
            request,
            "Daily record deleted successfully.",
        )

        return redirect(
            "daily_record_list"
        )

    return render(
        request,
        "daily_record_confirm_delete.html",
        {
            "record": record,
        },
    )


# ============================================================
# EGG PRODUCTION CRUD
# ============================================================

@login_required
def egg_production_list(request):

    owner_id = request.user.id

    egg_productions = (
        get_egg_productions_by_owner(
            owner_id
        )
    )

    return render(
        request,
        "egg_production_list.html",
        {
            "egg_productions": egg_productions,
        },
    )


@login_required
def egg_production_create(request):

    owner_id = request.user.id

    batches = get_batches_for_egg_production(
        owner_id
    )

    if request.method == "POST":

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        production_date = request.POST.get(
            "production_date",
            "",
        ).strip()

        egg_count = request.POST.get(
            "egg_count",
            "",
        ).strip()

        damaged_egg_count = request.POST.get(
            "damaged_egg_count",
            "",
        ).strip()

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            create_egg_production(
                owner_id=owner_id,
                batch_id=batch_id,
                production_date=production_date,
                egg_count=egg_count,
                damaged_egg_count=damaged_egg_count,
                notes=notes,
            )

            messages.success(
                request,
                "Egg production record created successfully.",
            )

            return redirect(
                "egg_production_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "An egg production record already exists for this batch and date.",
            )

    return render(
        request,
        "egg_production_form.html",
        {
            "batches": batches,
        },
    )


@login_required
def egg_production_update(
    request,
    egg_production_id,
):

    owner_id = request.user.id

    egg_production = (
        get_egg_production_by_id(
            egg_production_id=egg_production_id,
            owner_id=owner_id,
        )
    )

    batches = get_batches_for_egg_production(
        owner_id
    )

    if egg_production is None:

        messages.error(
            request,
            "Egg production record not found.",
        )

        return redirect(
            "egg_production_list"
        )

    if request.method == "POST":

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        production_date = request.POST.get(
            "production_date",
            "",
        ).strip()

        egg_count = request.POST.get(
            "egg_count",
            "",
        ).strip()

        damaged_egg_count = request.POST.get(
            "damaged_egg_count",
            "",
        ).strip()

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            update_egg_production(
                egg_production_id=egg_production_id,
                owner_id=owner_id,
                batch_id=batch_id,
                production_date=production_date,
                egg_count=egg_count,
                damaged_egg_count=damaged_egg_count,
                notes=notes,
            )

            messages.success(
                request,
                "Egg production record updated successfully.",
            )

            return redirect(
                "egg_production_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "An egg production record already exists for this batch and date.",
            )

    return render(
        request,
        "egg_production_form.html",
        {
            "egg_production": egg_production,
            "batches": batches,
        },
    )


@login_required
def egg_production_delete(
    request,
    egg_production_id,
):

    owner_id = request.user.id

    egg_production = (
        get_egg_production_by_id(
            egg_production_id=egg_production_id,
            owner_id=owner_id,
        )
    )

    if egg_production is None:

        messages.error(
            request,
            "Egg production record not found.",
        )

        return redirect(
            "egg_production_list"
        )

    if request.method == "POST":

        delete_egg_production(
            egg_production_id=egg_production_id,
            owner_id=owner_id,
        )

        messages.success(
            request,
            "Egg production record deleted successfully.",
        )

        return redirect(
            "egg_production_list"
        )

    return render(
        request,
        "egg_production_confirm_delete.html",
        {
            "egg_production": egg_production,
        },
    )


# ============================================================
# EXPENSE CRUD
# ============================================================

@login_required
def expense_list(request):

    owner_id = request.user.id

    expenses = get_expenses_by_owner(
        owner_id
    )

    return render(
        request,
        "expense_list.html",
        {
            "expenses": expenses,
        },
    )


@login_required
def expense_create(request):

    owner_id = request.user.id

    farms = get_farms_for_expense(
        owner_id
    )

    batches = get_batches_for_expense(
        owner_id
    )

    if request.method == "POST":

        farm_id = request.POST.get(
            "farm_id",
            "",
        ).strip()

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        expense_type = request.POST.get(
            "expense_type",
            "",
        ).strip()

        category = request.POST.get(
            "category",
            "",
        ).strip()

        amount = request.POST.get(
            "amount",
            "",
        ).strip()

        expense_date = request.POST.get(
            "expense_date",
            "",
        ).strip()

        description = request.POST.get(
            "description",
            "",
        ).strip()

        if not farm_id or not expense_type or not amount:

            messages.error(
                request,
                "Farm, expense type and amount are required.",
            )

            return render(
                request,
                "expense_form.html",
                {
                    "farms": farms,
                    "batches": batches,
                },
            )

        if expense_type == "FARM":

            batch_id = None

        elif expense_type == "BATCH":

            if not batch_id:

                messages.error(
                    request,
                    "Batch is required for batch expense.",
                )

                return render(
                    request,
                    "expense_form.html",
                    {
                        "farms": farms,
                        "batches": batches,
                    },
                )

        try:

            create_expense(
                owner_id=owner_id,
                farm_id=farm_id,
                batch_id=batch_id,
                expense_type=expense_type,
                category=category,
                amount=amount,
                expense_date=expense_date,
                description=description,
            )

            messages.success(
                request,
                "Expense created successfully.",
            )

            return redirect(
                "expense_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "Unable to create expense. Please check the selected farm and batch.",
            )

    return render(
        request,
        "expense_form.html",
        {
            "farms": farms,
            "batches": batches,
        },
    )


@login_required
def expense_update(
    request,
    expense_id,
):

    owner_id = request.user.id

    expense = get_expense_by_id(
        expense_id=expense_id,
        owner_id=owner_id,
    )

    farms = get_farms_for_expense(
        owner_id
    )

    batches = get_batches_for_expense(
        owner_id
    )

    if expense is None:

        messages.error(
            request,
            "Expense not found.",
        )

        return redirect(
            "expense_list"
        )

    if request.method == "POST":

        farm_id = request.POST.get(
            "farm_id",
            "",
        ).strip()

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        expense_type = request.POST.get(
            "expense_type",
            "",
        ).strip()

        category = request.POST.get(
            "category",
            "",
        ).strip()

        amount = request.POST.get(
            "amount",
            "",
        ).strip()

        expense_date = request.POST.get(
            "expense_date",
            "",
        ).strip()

        description = request.POST.get(
            "description",
            "",
        ).strip()

        if not farm_id or not expense_type or not amount:

            messages.error(
                request,
                "Farm, expense type and amount are required.",
            )

            return render(
                request,
                "expense_form.html",
                {
                    "expense": expense,
                    "farms": farms,
                    "batches": batches,
                },
            )

        if expense_type == "FARM":

            batch_id = None

        elif expense_type == "BATCH":

            if not batch_id:

                messages.error(
                    request,
                    "Batch is required for batch expense.",
                )

                return render(
                    request,
                    "expense_form.html",
                    {
                        "expense": expense,
                        "farms": farms,
                        "batches": batches,
                    },
                )

        try:

            update_expense(
                expense_id=expense_id,
                owner_id=owner_id,
                farm_id=farm_id,
                batch_id=batch_id,
                expense_type=expense_type,
                category=category,
                amount=amount,
                expense_date=expense_date,
                description=description,
            )

            messages.success(
                request,
                "Expense updated successfully.",
            )

            return redirect(
                "expense_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "Unable to update expense. Please check the selected farm and batch.",
            )

    return render(
        request,
        "expense_form.html",
        {
            "expense": expense,
            "farms": farms,
            "batches": batches,
        },
    )


@login_required
def expense_delete(
    request,
    expense_id,
):

    owner_id = request.user.id

    expense = get_expense_by_id(
        expense_id=expense_id,
        owner_id=owner_id,
    )

    if expense is None:

        messages.error(
            request,
            "Expense not found.",
        )

        return redirect(
            "expense_list"
        )

    if request.method == "POST":

        delete_expense(
            expense_id=expense_id,
            owner_id=owner_id,
        )

        messages.success(
            request,
            "Expense deleted successfully.",
        )

        return redirect(
            "expense_list"
        )

    return render(
        request,
        "expense_confirm_delete.html",
        {
            "expense": expense,
        },
    )


# ============================================================
# SALE CRUD
# ============================================================

@login_required
def sale_list(request):

    owner_id = request.user.id

    sales = get_sales_by_owner(
        owner_id
    )

    return render(
        request,
        "sale_list.html",
        {
            "sales": sales,
        },
    )


@login_required
def sale_create(request):

    owner_id = request.user.id

    farms = get_farms_for_sale(
        owner_id
    )

    batches = get_batches_for_sale(
        owner_id
    )

    if request.method == "POST":

        farm_id = request.POST.get(
            "farm_id",
            "",
        ).strip()

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        sale_type = request.POST.get(
            "sale_type",
            "",
        ).strip()

        unit = request.POST.get(
            "unit",
            "",
        ).strip()

        quantity = request.POST.get(
            "quantity",
            "",
        ).strip()

        unit_price = request.POST.get(
            "unit_price",
            "",
        ).strip()

        sale_date = request.POST.get(
            "sale_date",
            "",
        ).strip()

        buyer_name = request.POST.get(
            "buyer_name",
            "",
        ).strip()

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            create_sale(
                owner_id=owner_id,
                farm_id=farm_id,
                batch_id=batch_id,
                sale_type=sale_type,
                unit=unit,
                quantity=quantity,
                unit_price=unit_price,
                sale_date=sale_date,
                buyer_name=buyer_name,
                notes=notes,
            )

            messages.success(
                request,
                "Sale created successfully.",
            )

            return redirect(
                "sale_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "Unable to create sale. Please check the selected farm and batch.",
            )

    return render(
        request,
        "sale_form.html",
        {
            "farms": farms,
            "batches": batches,
        },
    )


@login_required
def sale_update(
    request,
    sale_id,
):

    owner_id = request.user.id

    sale = get_sale_by_id(
        sale_id=sale_id,
        owner_id=owner_id,
    )

    farms = get_farms_for_sale(
        owner_id
    )

    batches = get_batches_for_sale(
        owner_id
    )

    if sale is None:

        messages.error(
            request,
            "Sale not found.",
        )

        return redirect(
            "sale_list"
        )

    if request.method == "POST":

        farm_id = request.POST.get(
            "farm_id",
            "",
        ).strip()

        batch_id = request.POST.get(
            "batch_id",
            "",
        ).strip()

        sale_type = request.POST.get(
            "sale_type",
            "",
        ).strip()

        unit = request.POST.get(
            "unit",
            "",
        ).strip()

        quantity = request.POST.get(
            "quantity",
            "",
        ).strip()

        unit_price = request.POST.get(
            "unit_price",
            "",
        ).strip()

        sale_date = request.POST.get(
            "sale_date",
            "",
        ).strip()

        buyer_name = request.POST.get(
            "buyer_name",
            "",
        ).strip()

        notes = request.POST.get(
            "notes",
            "",
        ).strip()

        try:

            update_sale(
                sale_id=sale_id,
                owner_id=owner_id,
                farm_id=farm_id,
                batch_id=batch_id,
                sale_type=sale_type,
                unit=unit,
                quantity=quantity,
                unit_price=unit_price,
                sale_date=sale_date,
                buyer_name=buyer_name,
                notes=notes,
            )

            messages.success(
                request,
                "Sale updated successfully.",
            )

            return redirect(
                "sale_list"
            )

        except IntegrityError:

            messages.error(
                request,
                "Unable to update sale. Please check the selected farm and batch.",
            )

    return render(
        request,
        "sale_form.html",
        {
            "sale": sale,
            "farms": farms,
            "batches": batches,
        },
    )


@login_required
def sale_delete(
    request,
    sale_id,
):

    owner_id = request.user.id

    sale = get_sale_by_id(
        sale_id=sale_id,
        owner_id=owner_id,
    )

    if sale is None:

        messages.error(
            request,
            "Sale not found.",
        )

        return redirect(
            "sale_list"
        )

    if request.method == "POST":

        delete_sale(
            sale_id=sale_id,
            owner_id=owner_id,
        )

        messages.success(
            request,
            "Sale deleted successfully.",
        )

        return redirect(
            "sale_list"
        )

    return render(
        request,
        "sale_confirm_delete.html",
        {
            "sale": sale,
        },
    )