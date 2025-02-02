# Register Models in Admin
from django.contrib import admin
from .models import *

admin.site.register(Homepagebanner)
admin.site.register(Wishlist)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Couponcode)
admin.site.register(OrderItem)


# Inline for Additional Images
class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage
    extra = 1

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'collection', 'price', 'stock', 'is_active', 'updated_at')
    search_fields = ('name', 'sku')
    list_filter = ('is_active', 'collection', 'updated_at')
    inlines = [AdditionalImageInline]

# Register other product-related models
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_range', 'availability', 'updated_at')
    list_filter = ('category',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')




@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city', 'country', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('city', 'country')
