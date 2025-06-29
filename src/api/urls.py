from django.urls import path, include
from .views import ProviderList, ProviderDetail, OrderList, OrderDetail, ProviderRatingList, ProductRatingList

urlpatterns = [
    path('providers/', ProviderList.as_view()),
    path('providers/<int:pk>', ProviderDetail.as_view()),
    path('orders/', OrderList.as_view()),
    path('orders/<int:pk>', OrderDetail.as_view()),
    path('provider-ratings/', ProviderRatingList.as_view()),
    path('product-ratings/', ProductRatingList.as_view()),
]