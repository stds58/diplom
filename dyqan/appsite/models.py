from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}'


class Country(models.Model):
    country_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.country_name}'

    def get_absolute_url(self):
        x = 'country'
        return reverse(x, args=[str(self.id)])


class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.category_name}'

    def get_absolute_url(self):
        x = 'category'
        return reverse(x, args=[str(self.id)])


class Image(models.Model):
    img = models.ImageField(upload_to='images', unique=True)

    @property
    def photo_url(self):
        return format_html('<img src="{}" width="300" height="300" alt="">'.format(self.img.url))

    @property
    def photo_url_carusel(self):
        return format_html('src="{}" width="300" height="300" '.format(self.img.url))


    def __str__(self):
        return format_html('<img src="{}" width="100" height="100" alt="">'.format(self.img.url))

    def get_absolute_url(self):
        return reverse('imgs')


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    marka = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    quantity = models.PositiveIntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ManyToManyField('Image', through='ImageProduct')

    def __str__(self):
        return f'{self.product_name}'

    def get_absolute_url(self):
        x = 'product'
        return reverse(x, args=[str(self.id)])

    def add_product(self):
        print('product',111111)


class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(blank=True, null = True)
    product = models.ManyToManyField('Product', through='OrderProduct')
    date_create = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    date_delivery = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}'


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        x = 'orderproduct'
        return reverse(x, args=[str(self.id)])


class ImageProduct(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)