from django.shortcuts import render
from django.http import HttpResponse

def info(request):
    return render(request, template_name="info.html")

def home(request):
    categories = [
        {"category_name": "Комплектующие для ПК", "slug": "pc-parts"},
        {"category_name": "Ноутбуки", "slug": "laptops"},
        {"category_name": "Смартфоны", "slug": "smartphones"},
        {"category_name": "Планшеты", "slug": "tablets"},
        {"category_name": "Книги", "slug": "books"},
    ]
    return render(request, template_name="home.html", context={'categories': categories})

def category(request, category):
    goods = {
        "pc-parts": [
            {"good_name": "RTX 4080", "price": 9000, "status": "В наличии"},
            {"good_name": "Ryzen 9 9800X3D", "price": 4000, "status": "В наличии"},
        ],
        "laptops": [
            {"good_name": "Ноутбук ASUS", "price": 3000, "status": "В наличии"},
            {"good_name": "Ноутбук HP", "price": 2500, "status": "Под заказ"},
        ],
        "smartphones": [
            {"good_name": "iPhone 15", "price": 3600, "status": "В наличии"},
            {"good_name": "Samsung Galaxy S23", "price": 3000, "status": "Под заказ"},
        ],
        "tablets": [
            {"good_name": "iPad 11 Pro", "price": 1700, "status": "Под заказ"},
            {"good_name": "Samsung Tab S8", "price": 2000, "status": "В наличии"},
        ],
        "books": [
            {"good_name": "Война и мир", "price": 25, "status": "В наличии"},
            {"good_name": "Богатый папа, бедный папа", "price": 15, "status": "В наличии"},
        ],
    }

    categories = [
        {"category_name": "Комплектующие для ПК", "slug": "pc-parts"},
        {"category_name": "Ноутбуки", "slug": "laptops"},
        {"category_name": "Смартфоны", "slug": "smartphones"},
        {"category_name": "Планшеты", "slug": "tablets"},
        {"category_name": "Книги", "slug": "books"},
    ]

    category_name = next((category["category_name"] for category in categories if category["slug"] == category), "Неизвестная категория")
    return render(request, template_name="category.html", context={
        'goods': goods.get(category, []),
        'category_name': category_name,
    })

def goods(request):
    goods = [
        {"good_name": "RTX 4080", "price": 9000, "status": "В наличии", "category": "Комплектующие для ПК"},
        {"good_name": "Ryzen 9 9800X3D", "price": 4000, "status": "В наличии", "category": "Комплектующие для ПК"},
        {"good_name": "Ноутбук ASUS", "price": 3000, "status": "В наличии", "category": "Ноутбуки"},
        {"good_name": "Ноутбук HP", "price": 2500, "status": "Под заказ", "category": "Ноутбуки"},
        {"good_name": "iPhone 15", "price": 3600, "status": "В наличии", "category": "Смартфоны"},
        {"good_name": "Samsung Galaxy S23", "price": 3000, "status": "Под заказ", "category": "Смартфоны"},
        {"good_name": "iPad 11 Pro", "price": 1700, "status": "Под заказ", "category": "Планшеты"},
        {"good_name": "Samsung Tab S8", "price": 2000, "status": "В наличии", "category": "Планшеты"},
        {"good_name": "Война и мир", "price": 25, "status": "В наличии", "category": "Книги"},
        {"good_name": "Богатый папа, бедный папа", "price": 15, "status": "В наличии", "category": "Книги"},
    ]
    return render(request, template_name='goods.html', context={'goods': goods})

def users(request):
    users = [
        {"name": "Райан Рейнольдс", "age": 48, "phone": "+375291234567", "photo": "shop/img/users/raian.jpg"},
        {"name": "Роберт Дауни — младший", "age": 59, "phone": "+79871234321", "photo": "shop/img/users/robert-downey.jpg"},
        {"name": "Тоби Магуайр", "age": 49, "phone": "5555555555", "photo": "shop/img/users/toby_maguire.jpeg"},
        {"name": "Том Холланд", "age": 28, "phone": "1111111111", "photo": "shop/img/users/tom_holland.jpeg"},
        {"name": "Зендея Коулман", "age": 28, "phone": "9999999999", "photo": "shop/img/users/zendeya.jpg"},
    ]
    return render(request, template_name='users.html', context={'users': users})