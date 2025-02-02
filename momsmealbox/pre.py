
from home.models import *

def allpage(request):
    theme = Theme.objects.filter(display_in_home=True)[:3]
    collection = Collection.objects.filter(display_in_home=True)[:6]
    # Check if user is logged in, otherwise use session_id
    pre_wishlist = 0
    pre_cart = 0
    if request.user.is_authenticated:
        user = request.user
       
        pre_wishlist_master = Wishlist.objects.filter(user=user).first()
        for ie in pre_wishlist_master.product.all():
            pre_wishlist = pre_wishlist + 1
        try:
            cart_master = Cart.objects.filter(user=user).first()
            pre_cart = CartItem.objects.filter(cart=cart_master).count()
        except:
            pre_cart = 0
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        pre_wishlist_master = Wishlist.objects.filter(session_id=session_id).first()
        try:
            for ie in pre_wishlist_master.product.all():
                pre_wishlist = pre_wishlist + 1
        except:
            pass

        try:
            
            cart_master = Cart.objects.filter(session_id=session_id).first()
            pre_cart = CartItem.objects.filter(cart=cart_master).count()
        except:
            pre_cart = 0
    
    context ={
        'pre_theme':theme,
        'pre_collection':collection,
        'pre_wishlist':pre_wishlist, 'pre_cart':pre_cart,
        
    }
    return context