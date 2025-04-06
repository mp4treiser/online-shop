from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, ProductCategory

def info(request):
    return render(request, template_name="info.html")

def home(request):
    return render(request, template_name="home.html", context={'categories': ProductCategory.choices})


def category(request, category_slug):
    products = Product.objects.filter(category=category_slug)

    category_name = dict(ProductCategory.choices)[category_slug]

    return render(request, template_name="category.html", context={
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