from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('products', views.products, name='products'),
    path('quick_view/<int:id>', views.quick_view, name='quick_view'),
    path('viewcart', views.viewcart, name='viewcart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_cart_item/<int:item_id>', views.remove_cart_item, name='remove_cart_item'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('delete_wishlist_item/<int:id>', views.delete_wishlist_item, name='delete_wishlist_item'),
    path('add_to_wishlist/<int:product_id>', views.add_to_wishlist, name='addwish'),
    path('feedback', views.feedback, name='feedback'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('account_detail', views.account_detail, name='account_detail'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('order_history', views.order_history, name='order_history'),
    path('track_order', views.track_order, name='track_order'),

]