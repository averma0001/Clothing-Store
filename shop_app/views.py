from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date, timedelta


# Create your views here.

def home(request):
    products = Product.objects.all()
    productVariations = ProductVariation.objects.all()

    # cart items counting to show on every page of site 
    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)
        # Cart code end here 

        # wishlist code 
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

    context = {
        'products' : products,
        'productvariations' : productVariations,
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items': wish_items,
        'wish_len' : wish_len,
    }
    
    return render(request,'index.html', context)

def signup(request):
    if request.method == 'POST':
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['username']
        pswd1 = request.POST['password1']
        pswd2 = request.POST['password2']

        # Password match
        if pswd1 == pswd2:
            
            if User.objects.filter(username=email).exists():
                # email is already in use
                messages.error(request, "Email is already in use")
                return redirect("/signup")

            # Create a new user 
            User.objects.create_user(first_name=first_name, last_name=last_name, username=email, password=pswd1)
            # signup successful.
            messages.success(request, "Account created successfully. Please login!")
            
            return redirect("/login")

        else: 
            messages.error(request, "Passwords do not match")
            return redirect("/signup")
        
    # cart & wishlist code
    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)

        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    # cart & wishlist code ends
    
    context = {
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
    } 
        
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        # values fetch 
        email = request.POST['username']
        pswd = request.POST['password']

        # Authenticate 
        user = auth.authenticate(request, username=email, password=pswd)

            # If user found:
        if user is not None:
            # Login -> Redirect to home page
            auth.login(request, user)   # Start a Cookie-based session for the user 

            return redirect("/")
        else:
            # Message: Invalid credentials
            messages.error(request, "Invalid credentials. Please try again")
            # redirect back to login 
            return redirect("/login")
    
    # cart & wishlist code -->  
    
    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0
    
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    # cart & wishlist code ends

    context = {
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,

        }
    
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    messages.info(request,"You have logged Out")

    return redirect('/login')

def products(request):
    category = request.GET.get('category')
    if category=="Women":
        products = Product.objects.filter(category=category)
    elif category=="Men":
        products = Product.objects.filter(category=category)
    elif category=="Accessories":
        products = Product.objects.filter(category=category)
    elif category=="Bag":
        products = Product.objects.filter(category=category)
    elif category=="Shoes":
        products = Product.objects.filter(category=category)
    elif category=="Watches":
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    if request.method=="POST":
        search = request.POST['search']
        
        products = Product.objects.filter(  Q(category__istartswith=search) | 
                                            Q(name__icontains=search) |
                                            Q(brand__icontains=search)  )

    # cart & wishlist code -->

    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0
    
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    # cart & wishlist code ends

    context = {
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
        'products' : products

        }
    
    return render(request, 'products.html', context)

def quick_view(request, id):
    # cart & wishlist code

    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0

        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    # cart & wishlist code ends

    product = Product.objects.get(id=id)
    productV = ProductVariation.objects.filter(product_id=id)

    if productV.exists()==False:
        messages.error(request, "Sorry! This item is Out of Stock.")
        context = {
            'n_items' : n_items,
            'items' : items,
            'cart_total' : cart_total,
            'wish_items' : wish_items,
            'wish_len' : wish_len,
        }
        return render(request, 'stock_out.html', context)

    context = {
        'product': product,
        'productV': productV,
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
    }
    return render(request, 'quick_view.html', context)

def add_to_cart(request,id):
    
    if request.user.is_anonymous:
        messages.error(request, "Please, Login First!")
        return redirect('/login')

    if request.method=="POST":
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        color = request.POST['color']
        size = request.POST['size']
        quantity = request.POST['num-product']

        try:
            productv = ProductVariation.objects.get(product_id=id, color=color, size=size)
        except Exception:
            messages.error(request, "Sorry! This Combination is Out of Stock,  Please Choose different Size or Color.")
            return redirect(f'/quick_view/{id}')

        if OrderItem.objects.filter(productv=productv, order_id=order.id):
            messages.error(request, "Item is already in Cart. You can adjust its quantity.")
        else:
            OrderItem.objects.create(order_id=order.id, productv=productv, quantity=quantity, total_price=(productv.product.price)*int(quantity))
            messages.success(request, 'Item has been added to your Cart.')


    return redirect('/viewcart')

def viewcart(request):
    # cart & wishlist code also -->

    if request.user.is_anonymous:
        items = []
        n_items = 0
        items_price = []
        cart_total = 0
        wish_items = []
        wish_len = 0
        delivery_date = (date.today() + timedelta(days=3))
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        delivery_day = day_names[delivery_date.weekday()]
        date_str = delivery_date.strftime("%b %d")
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        items_price = []
        n_items = len(items)
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)
        delivery_date = (date.today() + timedelta(days=3))
        date_str = delivery_date.strftime("%b %d")
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        delivery_day = day_names[delivery_date.weekday()]

        for item in items:
            item_price = (item.productv.product.price) * (item.quantity)
            items_price.append(item_price)

        # Combine 'items' and 'items_price' into a single list of tuples using zip
    items_combined = list(zip(items, items_price))
    cart_total=sum(items_price)

    context = {
        'items_combined': items_combined,
        'cart_total' : cart_total,
        'n_items' : n_items,
        'items' : items,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
        'delivery_date' : date_str,
        'delivery_day' : delivery_day,
    }
    return render(request, 'shoping-cart.html', context)

def remove_cart_item(request, item_id):
    order, created = Order.objects.get_or_create(user=request.user, completed=False)

    cart_obj = OrderItem.objects.get(id=item_id, order_id=order.id)
    cart_obj.delete()

    return redirect('/viewcart')

def feedback(request):
    cust_email = request.POST['email']
    message = request.POST['msg']

    Feedback.objects.create(cust_email=cust_email, message=message)
    messages.success(request, "Thanks! We will get back to you shortly.")

    return redirect('/contact')

def about(request):

    # cart & wishlist code -->
    
    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    # cart & wishlist code ends

    context = {
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
    }

    return render(request, 'about.html', context)

def contact(request):

    # cart & wishlist code -->
    
    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    # cart & wishlist code ends

    context = {
        'n_items' : n_items,
        'items' : items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
        
    }

    return render(request, 'contact.html', context)


def delete_wishlist_item(request,id):
    wishlist_obj = Wishlist.objects.get(id=id)

    wishlist_obj.delete()
    print(id)
    
    return redirect('/wishlist')

def add_to_wishlist(request, product_id):
    if request.user.is_anonymous:
        messages.error(request, "Please, Login First!")
        return redirect('/login')

    try:
        product = Product.objects.get(id=product_id)

        Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({'message': f'"{product.name}" is added to wishlist successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def wishlist(request):
    #  cart & wishlist code 
    if request.user.is_anonymous:
        n_items= 0
        cart_total = 0
        items = []
        wish_items = []
        wish_len = 0
    else:
        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        n_items = len(items)
        cart_total = 0
        wish_items = Wishlist.objects.filter(user=request.user)
        wish_len = len(wish_items)

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)

    context = {
        'n_items' : n_items,
        'items': items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
        
    }

    # Cart code end here

    return render(request, 'wishlist.html', context)

def account_detail(request):
    #  cart & wishlist code 
    order, created = Order.objects.get_or_create(user=request.user, completed=False)
    items = OrderItem.objects.filter( order_id=order.id)
    n_items = len(items)
    cart_total = 0
    wish_items = Wishlist.objects.filter(user=request.user)
    wish_len = len(wish_items)
    for item in items:
        cart_total+=(item.productv.product.price * item.quantity)
    # Cart code end here

    user = request.user
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['email']

        user.first_name = first_name
        user.last_name = last_name
        user.username = username

        user.save()
        
        messages.success(request, 'Details Updated, Successfully.')

        return redirect('/account_detail')
    
    context = {
        'n_items' : n_items,
        'items': items,
        'cart_total' : cart_total,
        'wish_items' : wish_items,
        'wish_len' : wish_len,
        'user' : user  
    }
    
    return render(request, 'user_info.html',context)

def update_cart(request):
    product_id = request.GET.get('data-product-id')
    action = request.GET.get('action')

    order, created = Order.objects.get_or_create(user=request.user, completed=False)

    cart_obj = OrderItem.objects.get(id=product_id, order_id=order.id)
    
    if action=='plus':
        cart_obj.quantity+=1
        cart_obj.save()
    else :
        cart_obj.quantity-=1
        cart_obj.save()
        if cart_obj.quantity<1:
            cart_obj.delete()

    return redirect('/viewcart')

def checkout(request):
    if request.method == 'POST':
        user = request.user
        state = request.POST['state']
        city = request.POST['city']
        landmark = request.POST['landmark']
        postal_code = request.POST['postcode']
        name = request.POST['name']

        add = Address.objects.create(user=user, name=name, state=state, city=city, landmark=landmark, postal_code=postal_code)

        order, created = Order.objects.get_or_create(user=request.user, completed=False)
        items = OrderItem.objects.filter( order_id=order.id)
        cart_total = 0

        for item in items:
            cart_total+=(item.productv.product.price * item.quantity)
        
        order.completed=True
        order.address=add
        order.save()

    return HttpResponse("Congratulation! Your Order has been placed.")

def order_history(request):
    return HttpResponse("Need to implement.")

def track_order(request):
    return HttpResponse("Need to implement.")