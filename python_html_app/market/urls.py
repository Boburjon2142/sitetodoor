from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm


urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("kategoriya/<slug:slug>/", views.category_detail, name="category_detail"),
    path("mahsulot/<slug:slug>/", views.product_detail, name="product_detail"),
    path("about/", views.about_page, name="about"),
    path("contact/", views.contact_page, name="contact"),
    path("help/", views.help_page, name="help"),
    path("favorites/", views.favorites_page, name="favorites"),
    path("favorites/toggle/<int:product_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("compare/", views.compare_page, name="compare"),
    path("compare/toggle/<int:product_id>/", views.toggle_compare, name="toggle_compare"),
    path("compare/remove/<int:item_id>/", views.remove_compare_item, name="remove_compare_item"),
    path("cart/", views.cart_page, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/item/<int:item_id>/update/", views.update_cart_item, name="update_cart_item"),
    path("cart/item/<int:item_id>/delete/", views.delete_cart_item, name="delete_cart_item"),
    path("checkout/", views.checkout_page, name="checkout"),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("register/", views.register_page, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html", authentication_form=LoginForm),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile_dashboard, name="profile_dashboard"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("profile/orders/", views.profile_orders, name="profile_orders"),
    path("profile/complaints/", views.profile_complaints, name="profile_complaints"),
    path("profile/addresses/", views.profile_addresses, name="profile_addresses"),
    path("profile/addresses/<int:address_id>/delete/", views.delete_address, name="delete_address"),
    path("profile/notifications/", views.profile_notifications, name="profile_notifications"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/products/", views.admin_products, name="admin_products"),
    path("dashboard/products/new/", views.admin_product_create, name="admin_product_create"),
    path("dashboard/products/<int:product_id>/edit/", views.admin_product_edit, name="admin_product_edit"),
    path("dashboard/products/<int:product_id>/delete/", views.admin_product_delete, name="admin_product_delete"),
    path("dashboard/categories/", views.admin_categories, name="admin_categories"),
    path("dashboard/categories/new/", views.admin_category_create, name="admin_category_create"),
    path("dashboard/categories/<int:category_id>/edit/", views.admin_category_edit, name="admin_category_edit"),
    path("dashboard/orders/", views.admin_orders, name="admin_orders"),
    path("dashboard/complaints/", views.admin_complaints, name="admin_complaints"),
]
