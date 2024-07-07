
from .models import Account, Country, Category, Image, Product, Order, OrderProduct, ImageProduct
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import CategoryForm, CountryForm, ProductForm, OrderForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class ProductList(ListView):
    model = Product
    orderng = 'id'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 3


class ProductListAdmin(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('appsite.view_product')
    model = Product
    orderng = 'id'
    template_name = 'productsadmin.html'
    context_object_name = 'productsadmin'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(ProductListAdmin, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class ProductDetailAdmin(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = ('appsite.view_product')
    model = Product
    template_name = 'productadmin.html'
    context_object_name = 'productadmin'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(ProductDetailAdmin, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


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

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(ProductCreate, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class ProductUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('appsite.change_product')
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class ProductDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('appsite.delete_product')
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('products')

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(ProductDelete, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


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


class CategoryList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('appsite.view_category')
    model = Category
    orderng = 'id'
    template_name = 'categorys.html'
    context_object_name = 'categorys'
    paginate_by = 2

    def dispatch(self, request, *args, **kwargs):
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse( render_to_string('flatpages/error.html') )
        user_groups = user.groups.values('id','user','name')
        if not user_groups:
            return HttpResponse( render_to_string('flatpages/error.html') )
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CategoryList, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse( render_to_string('flatpages/error.html') )


class CategoryDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = ('appsite.view_category')
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CategoryDetail, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CategoryCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('appsite.add_category')
    form_class = CategoryForm
    model = Category
    template_name = 'category_edit.html'
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CategoryCreate, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CategoryUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('appsite.change_category')
    form_class = CategoryForm
    model = Category
    template_name = 'category_edit.html'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CategoryUpdate, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CategoryDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('appsite.delete_category')
    model = Category
    template_name = 'category_delete.html'
    success_url = reverse_lazy('categorys')

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CategoryDelete, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CountryList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('appsite.view_country')
    model = Country
    orderng = 'id'
    template_name = 'countrys.html'
    context_object_name = 'countrys'
    paginate_by = 3

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CountryList, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CountryDetail(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    permission_required = ('appsite.view_country')
    model = Country
    template_name = 'country.html'
    context_object_name = 'country'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CountryDetail, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CountryCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('appsite.add_country')
    form_class = CountryForm
    model = Country
    template_name = 'country_edit.html'
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CountryCreate, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class CountryUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('appsite.change_country')
    form_class = CountryForm
    model = Country
    template_name = 'country_edit.html'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CountryUpdate, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)



class CountryDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('appsite.delete_country')
    model = Country
    template_name = 'country_delete.html'
    success_url = reverse_lazy('countrys')

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(CountryDelete, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


class ImageList(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    permission_required = ('appsite.view_image')
    model = Image
    template_name = 'imgs.html'
    context_object_name = 'imgs'

    def dispatch(self, request, *args, **kwargs):
        template_name = render_to_string('flatpages/error.html')
        username = request.user
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/signup/')
        except MultipleObjectsReturned:
            return HttpResponse(render_to_string('flatpages/error.html'))
        user_groups = user.groups.values('id', 'user', 'name')
        if not user_groups:
            return HttpResponse(template_name)
        for user_group in user_groups:
            if user_group['user'] == user.id and user_group['name'] == 'staff':
                return super(ImageList, self).dispatch(request, *args, **kwargs)
            else:
                return HttpResponse(template_name)


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

