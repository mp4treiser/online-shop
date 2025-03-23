from django.urls import path

from .views import home, catalog, product_category

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<str:product_category>/', product_category, name='product_category'),
]
