from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User 
from .models import (
    ShopCategory,
    ParentCategory,
    SubCategory,
    Location,
    UserRole,
    User,
    Subscriber,
    ShopImage,
    Product,
    ProductImage,
    Review,
    ProductVariation,
    Order,
    ProductAttribute,
    Payment,
    ShippingAddress,
)

class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'category__name']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['name']

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email']
    exclude = ['created_by', 'updated_by']  # Exclude the fields from the admin form

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['user', 'shop_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['user__first_name', 'user__last_name', 'shop_name']

class ShopImageAdmin(admin.ModelAdmin):
    list_display = ['image']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_available', 'is_active']
    list_filter = ['is_available', 'is_active']
    search_fields = ['name', 'category__name']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating']

class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'price', 'stock']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'variation', 'quantity', 'created_at', 'status']
    list_filter = ['status']
    search_fields = ['user__username', 'product__name']

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'payment_method', 'payment_status']

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'address', 'city', 'postal_code', 'country']

admin.site.register(ShopCategory, ShopCategoryAdmin)
admin.site.register(ParentCategory, ParentCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(ShopImage, ShopImageAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)