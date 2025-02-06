from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.text import slugify


# Product Category Model
class Theme(models.Model):
    name = models.CharField(max_length=255)  # Category Name
    slug = models.SlugField(max_length=255, unique=True)
    meta = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/')  # Representative Image
    description = RichTextUploadingField()  # Brief Description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp
    display_in_home= models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Collection Name
    slug = models.SlugField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='collections')  # Category Relationship
    image = models.ImageField(upload_to='collections/')  # Representative Image
    description = RichTextUploadingField()   # Collection Description
    highlights = RichTextUploadingField()  # Key Highlights (e.g., "Cashmere Sweaters, Embroidered Polos")
    price_range = models.CharField(max_length=100, blank=True, null=True)  # Example: "$500 - $1000"
    availability = models.CharField(max_length=255, blank=True, null=True)  # Example: "Limited to 200 pieces worldwide"
    materials_craftsmanship =RichTextUploadingField()   # Details on materials and production
    occasion = RichTextUploadingField()   # Use case for the collection
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp
    display_in_home= models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Auto-generate slug from name
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # Collection Relationship
    sku = models.CharField(max_length=100, unique=True)
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    featured_image = models.ImageField(upload_to='products/', blank=True, null=True)
    additional_images = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.ManyToManyField(Size, null=True,blank=True)
    best_seller = models.BooleanField(default=True)
    inspiritation = models.BooleanField(default=False)
    favourite = models.BooleanField(default=True)
    timer= models.PositiveIntegerField(null=True,blank=True)
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']

    def __str__(self):
        return self.name

    
    
    

    
class AdditionalImage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='products/', blank=True, null=True)
    def __str__(self):
        return self.name




# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def cartitem(self):
        return CartItem.objects.filter(cart=self.id)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Cart with session {self.session_id}"

# Cart Item Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='cart_items', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    def totalprice(self):
        x = float(self.quantity)*float(self.product.price)
        return x
    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# Cart Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    product = models.ManyToManyField(Product, related_name="wishlist_product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.session_id)


class Homepagebanner(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, )
    tagline = models.CharField(max_length=1255, )
    link = models.CharField(max_length=255, blank=True, null=True)
    featured_image = models.ImageField(upload_to='homepage/', )
    def __str__(self):
        return str(self.name)
    


class Couponcode(models.Model):
    name = models.CharField(max_length=255)
    valid_upto = models.DateField()
    flat_discount = models.IntegerField(blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    percentage_max_amount = models.IntegerField(blank=True, null=True)
    max_redeem_limit = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.name}"
    

class CouponcodeUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Couponcode, on_delete=models.CASCADE, related_name='mycode')
    created_at = models.DateTimeField(auto_now_add=True)
    used =  models.BooleanField(default=False)
    
# Customer Model
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    session_id=models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    order_note = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    final_amount =models.FloatField(blank=True, null=True)
    coupon_code = models.TextField(blank=True, null=True)
    
    paid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=200, blank=True, null=True)    
    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-order_date']

    def __str__(self):
        return f"Order {self.id} - {self.customer.first_name} {self.customer.last_name}"

# Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Customer, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='order_items', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

