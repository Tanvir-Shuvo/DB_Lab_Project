from django.contrib import admin
from django.urls import path

from poultry import views


urlpatterns = [

    # ========================================================
    # ADMIN
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # ========================================================
    # HOME
    # ========================================================

    path(
        "",
        views.home,
        name="home",
    ),


    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        "register/",
        views.register_view,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),


    # ========================================================
    # DASHBOARD
    # ========================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),


    # ========================================================
    # GLOBAL SEARCH
    # ========================================================

    path(
        "search/",
        views.search_view,
        name="search",
    ),

    # ========================================================
    # FARM CRUD
    # ========================================================

    path(
        "farms/",
        views.farm_list,
        name="farm_list",
    ),

    path(
        "farms/create/",
        views.farm_create,
        name="farm_create",
    ),

    path(
        "farms/<int:farm_id>/edit/",
        views.farm_update,
        name="farm_update",
    ),

    path(
        "farms/<int:farm_id>/delete/",
        views.farm_delete,
        name="farm_delete",
    ),


    # ========================================================
    # BATCH CRUD
    # ========================================================

    path(
        "batches/",
        views.batch_list,
        name="batch_list",
    ),

    path(
        "batches/create/",
        views.batch_create,
        name="batch_create",
    ),

    path(
        "batches/<int:batch_id>/edit/",
        views.batch_update,
        name="batch_update",
    ),

    path(
        "batches/<int:batch_id>/delete/",
        views.batch_delete,
        name="batch_delete",
    ),


    # ========================================================
    # DAILY RECORD CRUD
    # ========================================================

    path(
        "daily-records/",
        views.daily_record_list,
        name="daily_record_list",
    ),

    path(
        "daily-records/create/",
        views.daily_record_create,
        name="daily_record_create",
    ),

    path(
        "daily-records/<int:record_id>/edit/",
        views.daily_record_update,
        name="daily_record_update",
    ),

    path(
        "daily-records/<int:record_id>/delete/",
        views.daily_record_delete,
        name="daily_record_delete",
    ),


    # ========================================================
    # EGG PRODUCTION CRUD
    # ========================================================

    path(
        "egg-production/",
        views.egg_production_list,
        name="egg_production_list",
    ),

    path(
        "egg-production/create/",
        views.egg_production_create,
        name="egg_production_create",
    ),

    path(
        "egg-production/<int:egg_production_id>/edit/",
        views.egg_production_update,
        name="egg_production_update",
    ),

    path(
        "egg-production/<int:egg_production_id>/delete/",
        views.egg_production_delete,
        name="egg_production_delete",
    ),


    # ========================================================
    # EXPENSE CRUD
    # ========================================================

    path(
        "expenses/",
        views.expense_list,
        name="expense_list",
    ),

    path(
        "expenses/create/",
        views.expense_create,
        name="expense_create",
    ),

    path(
        "expenses/<int:expense_id>/edit/",
        views.expense_update,
        name="expense_update",
    ),

    path(
        "expenses/<int:expense_id>/delete/",
        views.expense_delete,
        name="expense_delete",
    ),


    # ========================================================
    # SALE CRUD
    # ========================================================

    path(
        "sales/",
        views.sale_list,
        name="sale_list",
    ),

    path(
        "sales/create/",
        views.sale_create,
        name="sale_create",
    ),

    path(
        "sales/<int:sale_id>/edit/",
        views.sale_update,
        name="sale_update",
    ),

    path(
        "sales/<int:sale_id>/delete/",
        views.sale_delete,
        name="sale_delete",
    ),
]