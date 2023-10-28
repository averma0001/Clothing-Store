from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register([Product, ProductVariation, Order, Wishlist, Feedback, OrderItem, Address])
