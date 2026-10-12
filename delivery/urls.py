from django.urls import path
from . import views


urlpatterns = [

    # ========================================================
    # HOME
    # ========================================================

    path(
        '',
        views.index,
        name='index'
    ),


    # ========================================================
    # SIGNUP / SIGNIN
    # ========================================================

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'signin/',
        views.signin,
        name='signin'
    ),


    # ========================================================
    # CUSTOMER
    # ========================================================

    path(
        'customer_home/<str:username>/',
        views.customer_home,
        name='customer_home'
    ),

    path(
        'view_menu/<int:restaurant_id>/<str:username>/',
        views.view_menu,
        name='view_menu'
    ),

    path(
        'add_to_cart/<int:item_id>/<str:username>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'show_cart/<str:username>/',
        views.show_cart,
        name='show_cart'
    ),

    # Remove item from customer cart
    path(
        'remove_from_cart/<int:item_id>/<str:username>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
    
    path(
        'decrease_cart_item/<int:item_id>/<str:username>/',
        views.decrease_cart_item,
        name='decrease_cart_item'
    ),
    
    path(
        'increase_cart_item/<int:item_id>/<str:username>/',
        views.increase_cart_item,
        name='increase_cart_item'
    ),

    # Checkout
    path(
        'checkout/<str:username>/',
        views.checkout,
        name='checkout'
    ),

    # Orders
    path(
        'orders/<str:username>/',
        views.orders,
        name='orders'
    ),

    # Razorpay payment success
    path(
        'payment_success/<str:username>/',
        views.payment_success,
        name='payment_success'
    ),


    # ========================================================
    # ADMIN DASHBOARD
    # ========================================================

    path(
        'admin_home/',
        views.admin_home,
        name='admin_home'
    ),


    # ========================================================
    # ADMIN - RESTAURANT
    # ========================================================

    # Add Restaurant
    path(
        'add_restaurant/',
        views.add_restaurant,
        name='add_restaurant'
    ),

    # Show Restaurants
    path(
        'show_restaurants/',
        views.open_show_restaurant,
        name='open_show_restaurant'
    ),

    # Open Update Restaurant Page
    path(
        'update_restaurant/<int:restaurant_id>/',
        views.open_update_restaurant,
        name='open_update_restaurant'
    ),

    # Save Updated Restaurant
    path(
        'update_restaurant_save/<int:restaurant_id>/',
        views.update_restaurant,
        name='update_restaurant'
    ),

    # Delete Restaurant
    path(
        'delete_restaurant/<int:restaurant_id>/',
        views.delete_restaurant,
        name='delete_restaurant'
    ),


    # ========================================================
    # ADMIN - MENU MANAGEMENT
    # ========================================================

    # Manage Menu / Open Restaurant Menu
    path(
        'update_menu/<int:restaurant_id>/',
        views.open_update_menu,
        name='open_update_menu'
    ),

    # Add Menu Item
    path(
        'update_menu_save/<int:restaurant_id>/',
        views.update_menu,
        name='update_menu'
    ),

    # Update Existing Menu Item
    path(
        'update_item/<int:item_id>/',
        views.update_item,
        name='update_item'
    ),

    # Delete Menu Item
    path(
        'delete_item/<int:item_id>/',
        views.delete_item,
        name='delete_item'
    ),

]

