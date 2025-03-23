from django.urls import path

from .views import home, users, goods, info, category

urlpatterns = [
    path('', home, name='home'),
    path('info/', info, name='info'),
    path('users/', users, name='users'),
    path('goods/', goods, name='goods'),
    path('category/<slug:category_slug>/', category, name='category'),
]
