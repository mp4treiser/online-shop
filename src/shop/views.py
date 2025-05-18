from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Product, ProductCategory
from .models.forms import ProductForm, ProductFilterForm, ProductSearchForm


def info(request):
    return render(request, template_name="info.html")

def home(request):
    return render(request, template_name="home.html", context={'categories': ProductCategory.choices})


def category(request, category_slug):
    products = Product.objects.filter(category=category_slug)

    category_name = dict(ProductCategory.choices)[category_slug]

    return render(request, template_name="products/category.html", context={
        'products': products,
        'category_name': category_name
    })

def products(request):
    products = Product.objects.all()
    return render(request, template_name='products.html', context={'products': products})

def users(request):
    users = [
        {"name": "Райан Рейнольдс", "age": 48, "phone": "+375291234567", "photo": "shop/img/users/raian.jpg"},
        {"name": "Роберт Дауни — младший", "age": 59, "phone": "+79871234321", "photo": "shop/img/users/robert-downey.jpg"},
        {"name": "Тоби Магуайр", "age": 49, "phone": "5555555555", "photo": "shop/img/users/toby_maguire.jpeg"},
        {"name": "Том Холланд", "age": 28, "phone": "1111111111", "photo": "shop/img/users/tom_holland.jpeg"},
        {"name": "Зендея Коулман", "age": 28, "phone": "9999999999", "photo": "shop/img/users/zendeya.jpg"},
    ]
    return render(request, template_name='users.html', context={'users': users})

def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    filter_form = ProductFilterForm(request.GET)
    search_form = ProductSearchForm(request.GET)

    if filter_form.is_valid():
        min_price = filter_form.cleaned_data.get('min_price')
        max_price = filter_form.cleaned_data.get('max_price')
        category = filter_form.cleaned_data.get('category')

        if min_price is not None:
            products = products.filter(price__gte=float(min_price))
        if max_price is not None:
            products = products.filter(price__lte=float(max_price))
        if category:
            products = products.filter(category=category)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

    context = {
        'products': products,
        'filter_form': filter_form,
        'search_form': search_form,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})