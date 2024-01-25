from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Product, Category, Profile, Order, OrderEntry
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop/main')
        else:
            messages.info(request, 'username or password incorrect')

    context = {}
    return render(request, 'shop/login.html', context)


def regform(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'shop/register.html', context)


def main(request):
    try:
        category = Category.objects.all()
        product = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404('Product does not exist')
    context = {'products': product, 'category': category}
    return render(request, 'shop/base.html', context)


def products_view(request, ):
    contact_list = Product.objects.all()
    paginator = Paginator(contact_list, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'products': Product.objects.all(), "page_obj": page_obj}
    return render(request, 'shop/products.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404('Product does not exist')
    context = {'product': product}
    return render(request, 'shop/detail.html', context)


def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        raise Http404('Category does not exist')
    context = {'category': category}
    return render(request, 'shop/category.html', context)


def categories(request):
    try:
        category = Category.objects.all()
    except Category.DoesNotExist:
        raise Http404('Category does not exist')
    context = {'category': category}
    return render(request, 'shop/categories.html', context)


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST['id']
        product = get_object_or_404(Product, id=product_id)
        try:
            profile = Profile.objects.get(user=request.user)
            profile.save()
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
            profile.save()
        if not profile.shopping_cart:
            profile.shopping_cart = Order.objects.create(profile=profile)
            profile.save()
        try:
            order_entry = OrderEntry.objects.get(order=profile.shopping_cart, product=product)
        except OrderEntry.DoesNotExist:
            order_entry = OrderEntry.objects.create(order=profile.shopping_cart, product=product)
        order_entry.count += 1
        order_entry.save()
        return redirect('shop:product_detail', product_id)


@login_required(redirect_field_name='login')
def shopping_cart(request):
    try:
        profile = Profile.objects.get(user=request.user)
        profile.save()
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        profile.save()
    order_entry = OrderEntry.objects.filter(order=profile.shopping_cart).order_by('product')
    t = 0
    for i in OrderEntry.objects.filter(order=profile.shopping_cart):
        t += i.product.price * i.count
    context = {'order_entry': order_entry, 'total': t}

    return render(request, 'shop/shopping_cart.html', context)


def clear_order(request):
    profile = Profile.objects.get(user=request.user)
    OrderEntry.objects.filter(order=profile.shopping_cart).delete()
    return redirect('shop:shopping_cart')


def clear_concrete_order(request):
    product_id = request.POST['id']
    profile = Profile.objects.get(user=request.user)
    OrderEntry.objects.filter(order=profile.shopping_cart, product=product_id).delete()
    return redirect('shop:shopping_cart')


def update_count(request):
    if request.method == 'POST':
        count = request.POST['new']
        id = request.POST['id']
        if int(count) > 0:
            order = OrderEntry.objects.get(id=id)
            order.count = count
            order.save()
        else:
            order = OrderEntry.objects.get(id=id)
            order.delete()
    return redirect('shop:shopping_cart')


def make_order(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if profile.shopping_cart.order.exists():
            profile.shopping_cart.status = 'COMPLETED'
            profile.shopping_cart.save()
            profile.shopping_cart = Order.objects.create(profile=profile)
            profile.save()
            return redirect('shop:success_order') Reverse for 'author_detail' with arguments '('',)' not found. 1 pattern(s) tried: ['articles/author_detail/(?P<author_id>[^/]+)\\Z']
        else:
            return redirect('shop:shopping_cart')


@login_required(redirect_field_name='login')
def success_order(request):
    return render(request, 'shop/success_order.html')


@login_required(redirect_field_name='login')
def account(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    if 'first_name' in request.POST:
        first_name = request.POST['first_name']
        user.first_name = first_name
        user.save()
    if 'last_name' in request.POST:
        last_name = request.POST['last_name']
        user.last_name = last_name
        user.save()
    if 'email' in request.POST:
        email = request.POST['email']
        user.email = email
        user.save()
    order_entry = Order.objects.filter(profile=profile).filter(status='COMPLETED').order_by('-id')[:5]
    for i in order_entry:
        entries = i.order.all()
        amount = sum(j.count for j in entries)
        i.amount = amount
        count = sum(k.product.price * k.count for k in entries)
        i.count = count
        i.save()
    context = {'first_name': first_name, 'last_name': last_name, 'email': email, 'order': order_entry}
    return render(request, 'shop/account.html', context)


@login_required(redirect_field_name='login')
def order_history(request):
    profile = Profile.objects.get(user=request.user)
    order = Order.objects.filter(profile=profile).filter(status='COMPLETED').order_by('-id')[:5]
    contact_list = Order.objects.filter(profile=profile).filter(status='COMPLETED').order_by('-id')[:5]
    paginator = Paginator(contact_list, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    for i in page_obj:
        entries = i.order.all()
        i.entries = entries
        count = sum(k.product.price * k.count for k in entries)
        i.count = count
        amount = sum(j.count for j in entries)
        i.amount = amount
    context = {'order': order, "page_obj": page_obj}
    return render(request, 'shop/order_history.html', context)

# def products_view(request, ):
#     contact_list = Product.objects.all()
#     paginator = Paginator(contact_list, 5)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {'products': Product.objects.all(), "page_obj": page_obj}
#     return render(request, 'shop/products.html', context)


@login_required(redirect_field_name='login')
def repeat_order(request):
    if request.method == 'POST':

        profile = Profile.objects.get(user=request.user)
        OrderEntry.objects.filter(order=profile.shopping_cart).delete()

        id = request.POST['new_id']
        order = Order.objects.get(id=id)
        entry = OrderEntry.objects.filter(order=order)

        for i in entry:
            try:
                order_entry = OrderEntry.objects.get(order=profile.shopping_cart, product=i.product)
                order_entry.count = i.count
                order_entry.save()
            except OrderEntry.DoesNotExist:
                order_entry = OrderEntry.objects.create(order=profile.shopping_cart, product=i.product)
                order_entry.count = i.count
                order_entry.save()

        t = 0
        for i in OrderEntry.objects.filter(order=profile.shopping_cart):
            t += i.product.price * i.count

    return redirect('shop:shopping_cart')
