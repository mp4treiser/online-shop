from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать на главную страницу маркетплейса!")

def catalog(request):
    return HttpResponse("Здесь будут отображаться все категории товаров маркетплейса.")

def product_category(request, product_category):
    message = f"Вы выбрали категорию: {product_category}"
    return HttpResponse(message)