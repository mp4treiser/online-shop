from django.urls import path
from .views import home, users, info, category, product_form, product_update, product_detail
from .models.forms import ProductListView

urlpatterns = [
    path('', home, name='home'),
    path('info/', info, name='info'),
    path('users/', users, name='users'),
    path('category/<slug:category_slug>/', category, name='category'),
    path('products/add_product/', product_form, name='add_product'),
    path('products/<int:pk>/edit/', product_update, name='product_update'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
]
