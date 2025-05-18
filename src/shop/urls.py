from django.urls import path

from .views import home, users, products, info, category

urlpatterns = [
    path('', home, name='home'),
    path('info/', info, name='info'),
    path('users/', users, name='users'),
    path('products/', products, name='products'),
    path('category/<slug:category_slug>/', category, name='category'),
]
