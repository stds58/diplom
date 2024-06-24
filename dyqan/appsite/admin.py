from django.contrib import admin
from .models import Account, Country, Category, Image, Product, Order, OrderProduct, ImageProduct


admin.site.register(Account)
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ImageProduct)