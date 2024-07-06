
from .models import Account, Country, Category, Image, Product, Order, OrderProduct, ImageProduct
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CategoryForm, CountryForm, ProductForm, OrderForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string


class ProductList(ListView):
    model = Product
    orderng = 'id'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 3


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


def add_in_basket(request, pk):
    account = Account.objects.filter(user__username=request.user).values('id')
    if not account:
        user = User.objects.filter(username=request.user).values('id')
        if not user:
            return HttpResponseRedirect('/accounts/signup/')
        else:
            acc = Account.objects.create(user_id=user)
            acc.save()
            account = Account.objects.filter(user__username=request.user).values('id')
    account_id = account.values_list('id')[0][0]
    order = Order.objects.filter(account=account_id).filter(is_paid=False)
    if not order:
        order = Order.objects.create(account_id=account_id)
        order.save()
        order_id = order.id
    else:
        order_id = order.values_list('id')[0][0]
    product = OrderProduct.objects.filter(order_id=order_id).filter(product_id=pk)
    if not product:
        product = OrderProduct.objects.create(order_id_id=order_id, product_id_id=pk, quantity=1)
        product.save()
    else:
        quantity = product.values_list('quantity')[0][0] + 1
        OrderProduct.objects.filter(order_id=order_id).filter(product_id=pk).update(quantity=quantity)
    return HttpResponseRedirect(reverse('product', args=[str(pk)]))


def delete_from_basket(request, pk):
    account = Account.objects.filter(user__username=request.user).values('id')
    if not account:
        user = User.objects.filter(username=request.user).values('id')
        if not user:
            return HttpResponseRedirect('/accounts/signup/')
        else:
            acc = Account.objects.create(user_id=user)
            acc.save()
            account = Account.objects.filter(user__username=request.user).values('id')
    account_id = account.values_list('id')[0][0]
    order = Order.objects.filter(account=account_id).filter(is_paid=False)
    if not order:
        return HttpResponseRedirect(reverse('product', args=[str(pk)]))
    order_id = order.values_list('id')[0][0]
    product = OrderProduct.objects.filter(order_id=order_id).filter(product_id=pk)
    if product:
        if product.values_list('quantity')[0][0] >= 2:
            quantity = product.values_list('quantity')[0][0] - 1
            OrderProduct.objects.filter(order_id=order_id).filter(product_id=pk).update(quantity=quantity)
        else:
            order_id = product.values_list('order_id')[0][0]
            order = Order.objects.filter(id=order_id)
            order.delete()
            product.delete()
    return HttpResponseRedirect(reverse('product', args=[str(pk)]))


class ProductCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('appsite.add_product')
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
    success_url = ''

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        imgs = self.request.FILES.getlist('image')
        if imgs:
            for img in imgs:
                img_obj = Image(img = img)
                img_obj.save()
                post_img_obj = ImageProduct(product=product, image=img_obj)
                post_img_obj.save()
        return super().form_valid(form)


class ProductUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('appsite.change_product')
    form_class = ProductForm
    model = Product
    template_name = 'producty_edit.html'


class ProductDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('appsite.delete_product')
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('products')


class OrderList(ListView):
    model = Order
    orderng = 'id'
    template_name = 'orders.html'
    context_object_name = 'orders'
    paginate_by = 2


class OrderDetail(DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'


class OrderCreate(CreateView):
    form_class = OrderForm
    model = Order
    template_name = 'order_edit.html'
    success_url = ''

    def form_valid(self, form):
        product = form.save(commit=False)
        account = Account.objects.filter(username = self.request.user).values('id')
        account_id = account.values_list('id')[0][0]
        product.user_id = account_id
        product.save()
        return super().form_valid(form)


class OrderUpdate(UpdateView):
    form_class = OrderForm
    model = Order
    template_name = 'order_edit.html'


class OrderDelete(DeleteView):
    model = Order
    template_name = 'order_delete.html'
    success_url = reverse_lazy('orders')


class CategoryList(ListView):
    model = Category
    orderng = 'id'
    template_name = 'categorys.html'
    context_object_name = 'categorys'
    paginate_by = 2


class CategoryDetail(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


class CategoryCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('appsite.add_category')
    form_class = CategoryForm
    model = Category
    template_name = 'category_edit.html'
    success_url = ''


class CategoryUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('appsite.change_category')
    form_class = CategoryForm
    model = Category
    template_name = 'category_edit.html'


class CategoryDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('appsite.delete_category')
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('categorys')


class CountryList(ListView):
    model = Country
    orderng = 'id'
    template_name = 'countrys.html'
    context_object_name = 'countrys'
    paginate_by = 3


class CountryDetail(DetailView):
    model = Country
    template_name = 'country.html'
    context_object_name = 'country'


class CountryCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('appsite.add_country')
    form_class = CountryForm
    model = Country
    template_name = 'country_edit.html'
    success_url = ''


class CountryUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('appsite.change_country')
    form_class = CountryForm
    model = Country
    template_name = 'country_edit.html'



class CountryDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('appsite.delete_country')
    model = Country
    template_name = 'country_delete.html'
    success_url = reverse_lazy('countrys')


class ImageList(ListView):
    model = Image
    template_name = 'imgs.html'
    context_object_name = 'imgs'


class OrderProductDetail(DetailView):
    model = OrderProduct
    template_name = 'orderproduct.html'
    context_object_name = 'orderproduct'


def About(request):
    template_name = render_to_string('flatpages/about.html')
    return HttpResponse(template_name)


def Contact(request):
    template_name = render_to_string('flatpages/contact.html')
    return HttpResponse(template_name)

