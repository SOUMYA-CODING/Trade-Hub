from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    # Auth
    path('login/', views.user_login, name="login"),
    path('reset_password/', views.PasswordReset, name="PasswordReset"),
    path('logout_from_dashbaord/', views.logout_from_dashbaord, name="logout_from_dashbaord"),

    # Dashboard
    path('dashboard/', views.dashboard, name="dashboard"),

    # Shop Category
    path('shop_category/', views.shop_category, name="shop_category"),
    path('add_shop_category/', views.add_shop_category, name="add_shop_category"),
    path('update_shop_category/<int:id>', views.update_shop_category, name="update_shop_category"),
    path('delete_shop_category/<int:id>', views.delete_shop_category, name="delete_shop_category"),

    # Parent Category
    path('parent_category/', views.parent_category, name="parent_category"),
    path('add_parent_category/', views.add_parent_category, name="add_parent_category"),
    path('update_parent_category/<int:id>', views.update_parent_category, name="update_parent_category"),
    path('delete_parent_category/<int:id>', views.delete_parent_category, name="delete_parent_category"),

    # Sub Category
    path('sub_category/', views.sub_category, name="sub_category"),
    path('add_sub_category/', views.add_sub_category, name="add_sub_category"),
    path('update_sub_category/<int:id>', views.update_sub_category, name="update_sub_category"),
    path('delete_sub_category/<int:id>', views.delete_sub_category, name="delete_sub_category"),

    # Location
    path('location/', views.location, name="location"),
    path('add_location/', views.add_location, name="add_location"),
    path('update_location/<int:id>', views.update_location, name="update_location"),
    path('delete_location/<int:id>', views.delete_location, name="delete_location"),

    # User Roles (Groups)
    path('user_role/', views.user_role, name="user_role"),
    path('add_user_role/', views.add_user_role, name="add_user_role"),
    path('update_user_role/<int:id>', views.update_user_role, name="update_user_role"),
    path('delete_user_role/<int:id>', views.delete_user_role, name="delete_user_role"),

    # Subscriber
    path('subscriber_list/', views.subscriber_list, name="subscriber_list"),
]