from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import razorpay

from .models import (
    Customer,
    Item,
    Restaurant,
    Cart,
    CartItem
)


# ============================================================
# HOME
# ============================================================

def index(request):

    return render(
        request,
        "delivery/index.html"
    )


# ============================================================
# SIGNUP
# ============================================================

def open_signup(request):

    return render(
        request,
        "delivery/signup.html"
    )


def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")

        # Check duplicate username
        if Customer.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "delivery/signup.html",
                {
                    "error": "Username already exists!"
                }
            )

        Customer.objects.create(
            username=username,
            password=password,
            email=email,
            mobile=mobile,
            address=address
        )

        return redirect("signin")

    return render(
        request,
        "delivery/signup.html"
    )


# ============================================================
# SIGNIN
# ============================================================

def open_signin(request):

    return render(
        request,
        "delivery/signin.html"
    )


def signin(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # ----------------------------------------------------
        # ADMIN LOGIN
        # ----------------------------------------------------

        if (
            username == "admin"
            and password == "admin123"
        ):

            return redirect("admin_home")

        # ----------------------------------------------------
        # CUSTOMER LOGIN
        # ----------------------------------------------------

        try:

            customer = Customer.objects.get(
                username=username,
                password=password
            )

            return redirect(
                "customer_home",
                username=customer.username
            )

        except Customer.DoesNotExist:

            return render(
                request,
                "delivery/signin.html",
                {
                    "error": "Invalid username or password"
                }
            )

    return render(
        request,
        "delivery/signin.html"
    )


# ============================================================
# CUSTOMER HOME
# ============================================================

def customer_home(request, username):

    # Admin must not use customer pages
    if username == "admin":
        return redirect("admin_home")

    customer = get_object_or_404(
        Customer,
        username=username
    )

    restaurants = Restaurant.objects.all()

    return render(
        request,
        "delivery/customer_home.html",
        {
            "username": customer.username,
            "customer": customer,
            "restaurants": restaurants
        }
    )



# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_home(request):

    restaurantList = Restaurant.objects.all()

    total_items = Item.objects.count()

    return render(
        request,
        "delivery/admin_home.html",
        {
            "restaurants": restaurantList,
            "total_items": total_items
        }
    )


# ============================================================
# ADMIN - ADD RESTAURANT
# ============================================================

def add_restaurant(request):

    if request.method == "POST":

        name = request.POST.get("name")
        picture = request.POST.get("picture")
        cuisine = request.POST.get("cuisine")
        rating = request.POST.get("rating")

        # Check duplicate restaurant
        if Restaurant.objects.filter(
            name=name
        ).exists():

            return render(
                request,
                "delivery/add_restaurant.html",
                {
                    "error": "Restaurant already exists!"
                }
            )

        Restaurant.objects.create(
            name=name,
            picture=picture,
            cuisine=cuisine,
            rating=rating
        )

        return redirect("admin_home")

    return render(
        request,
        "delivery/add_restaurant.html"
    )


# ============================================================
# ADMIN - SHOW RESTAURANTS
# ============================================================

def open_show_restaurant(request):

    restaurantList = Restaurant.objects.all()

    return render(
        request,
        "delivery/show_restaurants.html",
        {
            "restaurantList": restaurantList
        }
    )


# ============================================================
# ADMIN - OPEN UPDATE RESTAURANT
# ============================================================

def open_update_restaurant(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    return render(
        request,
        "delivery/update_restaurant.html",
        {
            "restaurant": restaurant
        }
    )


# ============================================================
# ADMIN - UPDATE RESTAURANT
# ============================================================

def update_restaurant(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    if request.method == "POST":

        restaurant.name = request.POST.get(
            "name"
        )

        restaurant.picture = request.POST.get(
            "picture"
        )

        restaurant.cuisine = request.POST.get(
            "cuisine"
        )

        restaurant.rating = request.POST.get(
            "rating"
        )

        restaurant.save()

        return redirect("admin_home")

    return render(
        request,
        "delivery/update_restaurant.html",
        {
            "restaurant": restaurant
        }
    )


# ============================================================
# ADMIN - DELETE RESTAURANT
# ============================================================

def delete_restaurant(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    restaurant.delete()

    return redirect("admin_home")


# ============================================================
# ADMIN - MANAGE MENU
# ============================================================

def open_update_menu(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    itemList = restaurant.items.all()

    return render(
        request,
        "delivery/update_menu.html",
        {
            "restaurant": restaurant,
            "itemList": itemList
        }
    )


# ============================================================
# ADMIN - ADD MENU ITEM
# ============================================================

def update_menu(
    request,
    restaurant_id
):

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        picture = request.POST.get("picture")

        vegeterian = (
            request.POST.get("vegeterian") == "on"
        )

        # Duplicate item check
        if restaurant.items.filter(
            name=name
        ).exists():

            return render(
                request,
                "delivery/update_menu.html",
                {
                    "restaurant": restaurant,
                    "itemList": restaurant.items.all(),
                    "error": "This menu item already exists!"
                }
            )

        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            vegeterian=vegeterian,
            picture=picture
        )

        return redirect(
            "open_update_menu",
            restaurant_id=restaurant.id
        )

    return redirect(
        "open_update_menu",
        restaurant_id=restaurant.id
    )


# ============================================================
# ADMIN - UPDATE MENU ITEM
# ============================================================

def update_item(
    request,
    item_id
):

    item = get_object_or_404(
        Item,
        id=item_id
    )

    if request.method == "POST":

        item.name = request.POST.get(
            "name"
        )

        item.description = request.POST.get(
            "description"
        )

        item.price = request.POST.get(
            "price"
        )

        item.picture = request.POST.get(
            "picture"
        )

        item.vegeterian = (
            request.POST.get("vegeterian") == "on"
        )

        item.save()

        return redirect(
            "open_update_menu",
            restaurant_id=item.restaurant.id
        )

    return render(
        request,
        "delivery/edit_item.html",
        {
            "item": item,
            "restaurant": item.restaurant
        }
    )


# ============================================================
# ADMIN - DELETE MENU ITEM
# ============================================================

def delete_item(
    request,
    item_id
):

    item = get_object_or_404(
        Item,
        id=item_id
    )

    restaurant_id = item.restaurant.id

    item.delete()

    return redirect(
        "open_update_menu",
        restaurant_id=restaurant_id
    )


# ============================================================
# CUSTOMER - VIEW RESTAURANT MENU
# ============================================================

def view_menu(
    request,
    restaurant_id,
    username
):

    if username == "admin":

        return redirect("admin_home")

    restaurant = get_object_or_404(
        Restaurant,
        id=restaurant_id
    )

    itemList = restaurant.items.all()

    return render(
        request,
        "delivery/customer_menu.html",
        {
            "restaurant": restaurant,
            "itemList": itemList,
            "username": username
        }
    )


# ============================================================
# CUSTOMER - ADD TO CART
#
# This function is used from the MENU.
# It increases quantity if item already exists.
# After adding, it returns to the MENU.
# ============================================================

def add_to_cart(
    request,
    item_id,
    username
):

    if username == "admin":

        return redirect("admin_home")

    item = get_object_or_404(
        Item,
        id=item_id
    )

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart, created = Cart.objects.get_or_create(
        customer=customer
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item
    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect(
        "view_menu",
        restaurant_id=item.restaurant.id,
        username=username
    )


# ============================================================
# CUSTOMER - SHOW CART
# ============================================================

def show_cart(
    request,
    username
):

    if username == "admin":

        return redirect("admin_home")

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        cart_items = cart.cart_items.select_related(
            "item"
        )

        total_price = cart.total_price()

    else:

        cart_items = []

        total_price = 0

    return render(
        request,
        "delivery/cart.html",
        {
            "username": username,
            "customer": customer,
            "cart": cart,
            "cart_items": cart_items,
            "total_price": total_price
        }
    )


# ============================================================
# CUSTOMER - DELETE ITEM
# ============================================================

def remove_from_cart(
    request,
    item_id,
    username
):

    if username == "admin":

        return redirect("admin_home")

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        cart_item = CartItem.objects.filter(
            cart=cart,
            item_id=item_id
        ).first()

        if cart_item:

            cart_item.delete()

    return redirect(
        "show_cart",
        username=username
    )


# ============================================================
# CUSTOMER - DECREASE QUANTITY
# ============================================================

def decrease_cart_item(
    request,
    item_id,
    username
):

    if username == "admin":

        return redirect("admin_home")

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        cart_item = CartItem.objects.filter(
            cart=cart,
            item_id=item_id
        ).first()

        if cart_item:

            if cart_item.quantity > 1:

                cart_item.quantity -= 1

                cart_item.save()

            else:

                cart_item.delete()

    return redirect(
        "show_cart",
        username=username
    )


# ============================================================
# CUSTOMER - INCREASE QUANTITY
#
# IMPORTANT:
# This is separate from add_to_cart().
# It returns directly to the CART.
# ============================================================

def increase_cart_item(
    request,
    item_id,
    username
):

    if username == "admin":

        return redirect("admin_home")

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        cart_item = CartItem.objects.filter(
            cart=cart,
            item_id=item_id
        ).first()

        if cart_item:

            cart_item.quantity += 1

            cart_item.save()

    return redirect(
        "show_cart",
        username=username
    )


# ============================================================
# CUSTOMER - CHECKOUT
# ============================================================

def checkout(
    request,
    username
):

    if username == "admin":

        return redirect("admin_home")

    customer = get_object_or_404(
        Customer,
        username=username
    )

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    # --------------------------------------------------------
    # No cart
    # --------------------------------------------------------

    if not cart:

        return render(
            request,
            "delivery/checkout.html",
            {
                "username": username,
                "customer": customer,
                "cart": None,
                "cart_items": [],
                "total_price": 0,
                "error": "Your cart is empty!"
            }
        )

    # --------------------------------------------------------
    # Get CartItems
    # --------------------------------------------------------

    cart_items = cart.cart_items.select_related(
        "item"
    )

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    total_price = cart.total_price()

    # --------------------------------------------------------
    # Empty cart
    # --------------------------------------------------------

    if not cart_items.exists() or total_price <= 0:

        return render(
            request,
            "delivery/checkout.html",
            {
                "username": username,
                "customer": customer,
                "cart": cart,
                "cart_items": cart_items,
                "total_price": 0,
                "error": "Your cart is empty!"
            }
        )

    # --------------------------------------------------------
    # Convert Rupees to Paise
    # --------------------------------------------------------

    amount_in_paise = int(
        round(float(total_price) * 100)
    )

    # --------------------------------------------------------
    # Razorpay Client
    # --------------------------------------------------------

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    # --------------------------------------------------------
    # Create Razorpay Order
    # --------------------------------------------------------

    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": 1
    }

    order = client.order.create(
        data=order_data
    )

    # --------------------------------------------------------
    # Send Data To Checkout Page
    # --------------------------------------------------------

    return render(
        request,
        "delivery/checkout.html",
        {
            "username": username,
            "customer": customer,
            "cart": cart,
            "cart_items": cart_items,
            "total_price": total_price,

            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "razorpay_amount": amount_in_paise
        }
    )


# ============================================================
# CUSTOMER - ORDERS
# ============================================================

def orders(
    request,
    username
):

    customer = get_object_or_404(
        Customer,
        username=username
    )

    return render(
        request,
        "delivery/orders.html",
        {
            "username": username,
            "customer": customer
        }
    )


# ============================================================
# CUSTOMER - PAYMENT SUCCESS
# ============================================================

def payment_success(
    request,
    username
):

    # Payment verification must be POST
    if request.method != "POST":

        return redirect(
            "show_cart",
            username=username
        )

    customer = get_object_or_404(
        Customer,
        username=username
    )

    # --------------------------------------------------------
    # Get Razorpay details
    # --------------------------------------------------------

    payment_id = request.POST.get(
        "razorpay_payment_id"
    )

    razorpay_order_id = request.POST.get(
        "razorpay_order_id"
    )

    razorpay_signature = request.POST.get(
        "razorpay_signature"
    )

    # --------------------------------------------------------
    # Validate payment data
    # --------------------------------------------------------

    if (
        not payment_id
        or not razorpay_order_id
        or not razorpay_signature
    ):

        return render(
            request,
            "delivery/fail.html"
        )

    # --------------------------------------------------------
    # Razorpay Client
    # --------------------------------------------------------

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    # --------------------------------------------------------
    # Verify Razorpay signature
    # --------------------------------------------------------

    try:

        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": razorpay_signature
            }
        )

    except razorpay.errors.SignatureVerificationError:

        return render(
            request,
            "delivery/fail.html"
        )

    # --------------------------------------------------------
    # Get cart
    # --------------------------------------------------------

    cart = Cart.objects.filter(
        customer=customer
    ).first()

    if cart:

        # Make a list BEFORE deleting CartItems
        cart_items = list(
            cart.cart_items.select_related(
                "item"
            )
        )

        total_price = cart.total_price()

        # Clear cart after successful payment
        CartItem.objects.filter(
            cart=cart
        ).delete()

    else:

        cart_items = []

        total_price = 0

    # --------------------------------------------------------
    # Show successful order
    # --------------------------------------------------------

    return render(
        request,
        "delivery/orders.html",
        {
            "username": username,
            "customer": customer,
            "cart_items": cart_items,
            "total_price": total_price,
            "payment_id": payment_id
        }
    )

