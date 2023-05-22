from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    # Auth
    path('login/', views.user_login, name="login"),
    path('reset_password/', views.PasswordReset, name="PasswordReset"),
    path('logout/', views.logout, name="logout"),

    # Dashboard
    path('dashboard/', views.dashboard, name="dashboard"),

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
]