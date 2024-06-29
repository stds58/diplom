from django import forms
from .models import Account, Country, Category, Image, Product, Order, OrderProduct, ImageProduct


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'category_name',
        ]


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = [
            'country_name',
        ]


class ProductForm(forms.ModelForm):
    image = MultipleFileField(label='Select fotos', required=False)
    class Meta:
        model = Product
        fields = [
            'product_name',
            'marka',
            'price',
            'quantity',
            'country',
            'category'
        ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'product',
        ]



