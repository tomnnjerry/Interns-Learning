from django.urls import path
from . import views
app_name='home'
urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('products/<str:pk>/', views.products, name='products'),
    path('product-detail/<str:pk>/', views.product_detail, name='product_detail'), 

    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('quick-add-product/', views.quick_add_product, name='quick_add_product'),
    
    
    path('quick-view-product/', views.quick_view_product, name='quick_view_product'),
    path('add-to-cart-view/', views.add_to_cart_view, name='add_to_cart_view'),

    
    path('stock-check-ajax/', views.stock_check_ajax, name='stock_check_ajax'),
    path('cart-data-alter-ajax/', views.cart_data_alter, name='cart_data_alter'),
    path('wishlist/', views.wishlist, name='wishlist'),
    


    # static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),

    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('returns-and-exchange/', views.returns_exchange, name='returns_exchange'),
    path('shipping-policy/', views.shipping_policy, name='shipping_policy'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
    path('terms-and-conditions/', views.terms_conditions, name='terms_conditions'),
    path('view-wishlist/', views.view_wishlist, name='view_wishlist'),
    
    path('cart/', views.cart, name='cart'),
    path('remove-cart-item/', views.cart_removal, name='cart_removal'),

    path('checkout/', views.checkout, name='checkout'),
    path('check-coupon-code/', views.checkcouponcode, name='checkcouponcode'),

    path('payment/', views.paynow, name='pay'),
    path('payment_status', views.payment_status, name = 'payment_status'),

    #dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('address/', views.address, name='address'),
    path('profile/', views.profile, name='profile'),


] 
