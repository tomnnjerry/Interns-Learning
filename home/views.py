from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
import razorpay
client = razorpay.Client(auth=("rzp_test_BAFmlfpAivgV6F", "KoJLJSBgmGnxCwUxfMXYyzoY"))

# Create your views here.

def home(request):
    banner =  Homepagebanner.objects.all().order_by('-id')[:4]
    best_seller = Product.objects.filter(best_seller=True)[:8]
    favourite = Product.objects.filter(favourite=True)[:4]
    context = {
        'banner':banner,
        'best_seller':best_seller,
        'favourite':favourite,
    }
    return render(request, 'index.html', context)


def about(request):
    best_seller = Product.objects.filter(best_seller=True)[:8]
    
    context = {
        'best_seller':best_seller,
        
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    
    context = {
    }
    return render(request, 'pages/contact.html', context)

def faq(request):
    
    context = {
    }
    return render(request, 'pages/faq.html', context)

def privacy_policy(request):
    context = {}
    return render(request, 'pages/privacy_policy.html', context)

def returns_exchange(request):
    context = {}
    return render(request, 'pages/returns_exchange.html', context)

def shipping_policy(request):
    context = {}
    return render(request, 'pages/shipping_policy.html', context)
def refund_policy(request):
    context = {}
    return render(request, 'pages/refund_policy.html', context)

def terms_conditions(request):
    context = {}
    return render(request, 'pages/terms_conditions.html', context)


def view_wishlist(request):

    if request.user.is_authenticated:
        user = request.user
        data1 = Wishlist.objects.filter(user=user)
    else:
        session_id = request.session.session_key
        data1 = Wishlist.objects.filter(session_id=session_id)
    
    page = request.GET.get('page', 1)

    
    paginator = Paginator(data1, 6)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

 
    context = {
        'data':data,
    }
    return render(request, 'pages/wishlist.html', context)


def cart(request):

    if request.user.is_authenticated:
        user = request.user
        data = Cart.objects.filter(user=user)
    else:
        session_id = request.session.session_key
        data = Cart.objects.filter(session_id=session_id)
    
    context = {
        'data':data,
    }
    return render(request, 'cart/cart.html', context)


@csrf_exempt
def cart_removal(request):

    if request.user.is_authenticated:
        user = request.user
        data = Cart.objects.filter(user=user).first()

    else:
        session_id = request.session.session_key
        data = Cart.objects.filter(session_id=session_id).first()
    
    if data:
        if request.method=='POST':
            product_id = request.POST.get('product_id')
            product = CartItem.objects.get(id=product_id, cart=data)
            product.delete()
            classname = "number-"+str(product_id)

    return JsonResponse({'classname': classname})        



@csrf_exempt
def cart_data_alter(request):
    if request.user.is_authenticated:
        user = request.user
        data = Cart.objects.filter(user=user).first()

    else:
        session_id = request.session.session_key
        data = Cart.objects.filter(session_id=session_id).first()
    
    if data:
        if request.method=='POST':
            product_id = request.POST.get('product_id')
            value = request.POST.get('value')
            operate = request.POST.get('operate')
            value = int(value)
            operate = str(operate)
            
            product = CartItem.objects.get(id=product_id, cart=data)
            limit = value + 1
            
            if operate == 'plus':
                if int(product.product.stock) > limit:
                    product.quantity =  int(product.quantity)+1
                    product.save() 

            if operate == 'minus':
                if value > 1:
                    product.quantity =  int(product.quantity)-1
                    product.save()   

            
            new_subtotal = float(product.product.price)*float(product.quantity)
            mynumber = ".number-"+str(product_id)
            total = ".number_total-"+str(product_id)
            
    return JsonResponse({'new_subtotal': new_subtotal, 'quantity':product.quantity, 'mynumber':mynumber,'total':total}) 





def product(request):
    data1 = Product.objects.all().order_by('id')
    page = request.GET.get('page', 1)

    
    paginator = Paginator(data1, 6)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)


    context = {
        'data':data,
    }
    return render(request, 'product.html', context)


def products(request, pk):
    context = {

    }
    return render(request, 'products.html', context)

def product_detail(request, pk):
    product = Product.objects.get(slug=pk)
    related_product = Product.objects.all()
    context = {
        'product':product,
        'related_product':related_product,
    }
    return render(request, 'product_detail/product_detail.html', context)


def checkout(request):
    pre_cart = None
    if request.user.is_authenticated:
        user = request.user
        try:
            cart_master = Cart.objects.filter(user=user).first()
            pre_cart = CartItem.objects.filter(cart=cart_master)
        except:
            pass
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        try:
            
            cart_master = Cart.objects.filter(session_id=session_id).first()
            pre_cart = CartItem.objects.filter(cart=cart_master)
        except:
            pass
    total = 0
    if pre_cart is None:
        pass
    else:
        for i in pre_cart:
            total = (float(i.quantity)*float(i.product.price)) + total


    context ={
        'cart_item':pre_cart,
        'total':total,
        
    }
    
    return render(request, 'cart/checkout.html', context)





@csrf_exempt
def checkcouponcode(request):
    

    if request.method=='POST':
        code = request.POST.get('code')
        # Get product instance
        code = str(code)
        try:
            today = date.today() 
            match_code = Couponcode.objects.get(name=code, valid_upto__gt=today)
            print(match_code)
            limit = int(match_code.max_redeem_limit)
            total_price = 0
            if request.user.is_authenticated:
                cart_master = Cart.objects.filter(user=request.user).first()
                pre_cart = CartItem.objects.filter(cart=cart_master)
                for i in pre_cart:
                    total_price = (float(i.quantity)*float(i.product.price)) + total_price
                code_usage = CouponcodeUsage.objects.filter(user=request.user, code=match_code, used=True).count()
                if code_usage >= limit :
                    return JsonResponse({'item': 'Coupon Limit'})
                else:
                    code_usage = CouponcodeUsage.objects.create(user=request.user, code=match_code)
                    
                    # Calculate the discount
                    if match_code.flat_discount:  # Apply flat discount
                        discount = match_code.flat_discount
                    else:  # Apply percentage or percentage max amount
                        percentage_discount = (match_code.percentage / 100) * total_price
                        discount = min(percentage_discount, match_code.percentage_max_amount)

                    final_amount = total_price - discount
                    
                    return JsonResponse({'final_amount':final_amount, 'discount':discount, 'code':code, 'pass':'pass'}) 



            else:
                return JsonResponse({'item': 'invalid_code'})
            
        except:
            print('invalid code')
            return JsonResponse({'item': 'invalid_code'})
        
     
    
        
    
    return JsonResponse({'item': 'a'})



@csrf_exempt
def quick_add_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        context = {
            'product': product,
        }
        html = render_to_string('quick_add/quick_add_child.html', context, request=request)
        
    return JsonResponse({'html': html})

@csrf_exempt
def stock_check_ajax(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        stock = product.stock
        price = product.price
    return JsonResponse({'stock': stock, 'price':price})




@csrf_exempt
def quick_view_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        context = {
            'product': product,
        }
        html = render_to_string('quick_view/quick_view_child.html', context, request=request)
        
    return JsonResponse({'html': html})


@csrf_exempt
def add_to_cart_view(request):
   
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        qty = request.POST.get('qty')
        size = request.POST.get('size')
        qty = int(qty)
        print('hey', qty)
        # Get product instance
        product = get_object_or_404(Product, id=product_id)
        
        # Get size instance
        size = get_object_or_404(Size, name=size)
        
       
        # Check if user is logged in, otherwise use session_id
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id)
        
        
        # Check if the CartItem exists
        cart_item = CartItem.objects.filter(cart=cart, product=product, size=size).first()
        if cart_item:
            # If it exists, update the quantity
            cart_item.quantity = qty
            message = "CartItem updated successfully."
        else:
            # If it doesn't exist, create a new CartItem
            cart_item = CartItem(cart=cart, product=product, size=size, quantity=qty)
            message = "CartItem created successfully."
        
        # Save the CartItem
        cart_item.save()
        
        # Return response
        return JsonResponse({
            'message': 'Product added to cart successfully',
            'cart_item_id': cart_item.id,
            'quantity': cart_item.quantity,
            
        })

@csrf_exempt
def add_to_cart(request):
   
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        qty = request.POST.get('qty')
        size = request.POST.get('size')
        qty = int(qty)
        
        # Get product instance
        product = get_object_or_404(Product, id=product_id)
        
        # Get size instance
        size = get_object_or_404(Size, name=size)
        
       
        # Check if user is logged in, otherwise use session_id
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id)
        
        # Check if the CartItem exists
        cart_item = CartItem.objects.filter(cart=cart, product=product, size=size).first()
        if cart_item:
            # If it exists, update the quantity
            cart_item.quantity = qty
            message = "CartItem updated successfully."
        else:
            # If it doesn't exist, create a new CartItem
            cart_item = CartItem(cart=cart, product=product, size=size, quantity=qty)
            message = "CartItem created successfully."
        
        # Save the CartItem
        cart_item.save()
        initial_cart_count = CartItem.objects.filter(cart=cart).count()
       
        # Return response
        return JsonResponse({
            'message': 'Product added to cart successfully',
            'cart_item_id': cart_item.id,
            'quantity': cart_item.quantity,
            'final_cart_count':initial_cart_count,
            
        })
@csrf_exempt
def wishlist(request):
    # Check if user is logged in, otherwise use session_id
    a = 0
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        wishlist, created = Wishlist.objects.get_or_create(session_id=session_id)

    if request.method=='POST':
        product_id = request.POST.get('product_id')
        # Get product instance
        product = get_object_or_404(Product, id=product_id)
        product_data =wishlist.product.all()
        if product in product_data:
            wishlist.product.remove(product)
            wishlist.save()
            a = False
        else:
            wishlist.product.add(product)
            wishlist.save()
            a = True
        classname = ".wish"+str(product_id)
    return JsonResponse({'item': a, 'class':classname})




def paynow(request):
    if request.method=="POST":
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        # Fetch data directly from request.POST
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        country = request.POST.get("country")
        city = request.POST.get("city")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        order_note = request.POST.get("note")
        coupon_code = request.POST.get("coupon_code")
        payment_id = request.POST.get("payment_id", None)  # Optional field

        print(first_name)
        # Check if the customer already exists based on email or session_id
        customer, created = Customer.objects.get_or_create(
            email=email,
            defaults={
                "session_id": session_id,
                "first_name": first_name,
                "last_name": last_name,
                "country": country,
                "city": city,
                "address": address,
                "phone": phone,
                "order_note": order_note,
                "coupon_code": coupon_code,
                "payment_id": payment_id,
            },
        )
        print(customer)
        total_price = 0
        if request.user.is_authenticated:
            cart_master = Cart.objects.filter(user=request.user).first()
            pre_cart = CartItem.objects.filter(cart=cart_master)
            for i in pre_cart:
                total_price = (float(i.quantity)*float(i.product.price)) + total_price
        else:
            cart_master = Cart.objects.filter(session_id=session_id).first()
            pre_cart = CartItem.objects.filter(cart=cart_master)
            for i in pre_cart:
                total_price = (float(i.quantity)*float(i.product.price)) + total_price
            
        final_amount = float(total_price)   
        final_amount = round(final_amount, 2) 
        print(final_amount)
        if customer.coupon_code:
            code = str(customer.coupon_code)
            print(code)
            try:
                today = date.today() 
                match_code = Couponcode.objects.get(name=code, valid_upto__gt=today)
                print(match_code)
                limit = int(match_code.max_redeem_limit)
                total_price = 0
                if request.user.is_authenticated:
                    code_usage = CouponcodeUsage.objects.filter(user=request.user, code=match_code, used=True).count()
                    if code_usage >= limit :
                        return JsonResponse({'item': 'Coupon Limit'})
                    else:
                        code_usage = CouponcodeUsage.objects.create(user=request.user, code=match_code)
                        
                        # Calculate the discount
                        if match_code.flat_discount:  # Apply flat discount
                            discount = match_code.flat_discount
                        else:  # Apply percentage or percentage max amount
                            percentage_discount = (match_code.percentage / 100) * total_price
                            discount = min(percentage_discount, match_code.percentage_max_amount)

                        final_amount = total_price - discount
                        return JsonResponse({'final_amount':final_amount, 'discount':discount, 'code':code, 'pass':'pass'}) 



                else:
                    return JsonResponse({'item': 'invalid_code'})
                
            except:
                print('invalid code')
                return JsonResponse({'item': 'invalid_code'})
            
        

        order_amount = float(final_amount)*100
        print(order_amount)
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'welcome': 'Koxari - Luxuries'}

        # CREAING ORDER
        response = client.order.create(dict(amount=int(order_amount), currency=order_currency, receipt=order_receipt, notes=notes, payment_capture=0))
        order_id = response['id']
        order_status = response['status']
        customer.payment_id = order_id
        customer.final_amount= float(final_amount)
        customer.save()
        if order_status=='created':

            context = {
                'product_id':product,
                'price':final_amount,
                'name':customer.first_name,
                'phone':phone,
                'email':email,
                'order_id':order_id,
              
            }
            

            return render(request, 'cart/confirm_order.html', context)


        # print('\n\n\nresponse: ',response, type(response))
    return HttpResponse('<h1>Error in  create order function</h1>')

@csrf_exempt
def payment_status(request):

    response = request.POST

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
    for key , val in response.items():
        if key == "razorpay_order_id":
            order_id = val
            break
    order = Customer.objects.filter(payment_id=order_id).first()
    print(order)
    order.paid = True
    # Check if user is logged in, otherwise use session_id
    if request.user.is_authenticated:
        user = request.user
        data = Cart.objects.filter(user=user).first()

    else:
        session_id = request.session.session_key
        data = Cart.objects.filter(session_id=session_id).first()
    
    product = CartItem.objects.filter(cart=data)
    for ie in product:
        orderitem = OrderItem.objects.create(order=order, product=ie.product, size=ie.size, quantity=ie.quantity)
        orderitem.save()
        ie.delete()


    order.save() 
    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)
        return render(request, 'cart/order_summary.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'cart/order_summary.html', {'status': 'Payment Faliure!!!'})


 


 
def dashboard(request):
    context = {

    }
    return render(request, 'account/dashboard.html', context)

def address(request):
    context = {

    }
    return render(request, 'account/address.html', context)


def profile(request):
    context = {

    }
    return render(request, 'account/profile.html', context)

