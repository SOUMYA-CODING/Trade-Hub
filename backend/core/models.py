from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must be a 10-digit number.'
)

pin_code_validator = RegexValidator(
    regex=r'^\d{6}$',
    message='Pin code must be a 6-digit number.'
)

IS_ACTIVE_CHOICES = (
    (True, 'Active'),
    (False, 'Inactive'),
)

ORDER_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)

class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_created')
    updated_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='%(class)s_updated')

    class Meta:
        abstract = True

class ShopCategory(BaseModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES, default=True)

    def __str__(self):
        return self.name

class ParentCategory(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    icon = models.ImageField(upload_to='parent_category/', null=False)
    code = models.CharField(max_length=4, unique=True)
    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES, default=True)

    def __str__(self):
        return self.name

class SubCategory(BaseModel):
    category = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=8)
    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES, default=True)

    def __str__(self):
        return self.name

class Location(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserRole(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    present_address = models.TextField(max_length=200)
    permanent_address = models.TextField(max_length=200)
    pin_code = models.CharField(max_length=10, validators=[pin_code_validator])
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, validators=[phone_number_validator])

class Subscriber(BaseModel):
    # Subscriber details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=12, null=True)
    aadhar_photo = models.ImageField(upload_to='aadhar_photo/', null=True)
    pan_number = models.CharField(max_length=12, null=True)
    pan_photo = models.ImageField(upload_to='pan_photo/', null=True)

    # Shop details
    shop_type = models.ForeignKey(ShopCategory, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_establishment_date = models.DateField()
    number_of_employees = models.IntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    shop_phone = models.CharField(max_length=10, validators=[phone_number_validator])
    shop_email = models.EmailField()
    shop_address = models.CharField(max_length=200)
    is_shop_on_rented = models.BooleanField(null=True)

    # Documents
    shop_logo = models.ImageField(upload_to='shop_logos/')
    shop_images = models.ManyToManyField('ShopImage', related_name='shops')
    trade_agreement_certificate = models.FileField(upload_to='trade_agreements/')
    gst_number = models.CharField(max_length=100)
    shop_target_location = models.CharField(max_length=100)

    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES, default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class ShopImage(models.Model):
    image = models.ImageField(upload_to='shop_images/')

    def __str__(self):
        return self.image.name

class Product(BaseModel):
    user = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, related_name='products')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=12, unique=True)
    description = models.TextField()
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    is_on_discount = models.BooleanField(default=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ManyToManyField('ProductImage', related_name='products')
    promo_video = models.FileField(upload_to='promo_videos/', null=True, blank=True)
    is_active = models.BooleanField(choices=IS_ACTIVE_CHOICES, default=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.image.name

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='Pending')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)

class Payment(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Payment for Order {self.order.id}"

class ShippingAddress(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)