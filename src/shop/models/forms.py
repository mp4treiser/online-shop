from django import forms
from django.views.generic import ListView
from django.core.exceptions import ValidationError

from ..models import Product, ProductCategory
from django.db import models

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'count_items', 'description', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите название продукта'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Введите цену продукта'}),
            'count_items': forms.NumberInput(attrs={'placeholder': 'Введите количество товара'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [
            choice for choice in ProductCategory.choices 
            if choice[0] != ProductCategory.DEFAULT
        ]

    def clean(self):
        cleaned_data = super().clean()
        count_items = cleaned_data.get('count_items')
        is_available = cleaned_data.get('is_available')

        if count_items == 0 and is_available:
            raise ValidationError(
                'Товар не может быть доступен к продаже, если его количество равно 0'
            )
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 1:
            raise ValidationError('Цена не может быть меньше 1')
        return price


class ProductFilterForm(forms.Form):
    min_price = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Минимальная цена',
            'step': '0.01'
        })
    )
    max_price = forms.FloatField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Максимальная цена',
            'step': '0.01'
        })
    )
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'Все категории')] + [
            choice for choice in ProductCategory.choices 
            if choice[0] != ProductCategory.DEFAULT
        ]
    )

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price is not None and max_price is not None and min_price > max_price:
            raise ValidationError('Минимальная цена не может быть больше максимальной')
        return cleaned_data


class ProductSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по названию или описанию',
            'class': 'form-control'
        })
    )

    def search(self):
        query = self.cleaned_data.get('query')
        if query:
            return Product.objects.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )
        return Product.objects.all()


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = ProductFilterForm(self.request.GET)
        self.search_form = ProductSearchForm(self.request.GET)

        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data
            if data.get('min_price'):
                queryset = queryset.filter(price__gte=data['min_price'])
            if data.get('max_price'):
                queryset = queryset.filter(price__lte=data['max_price'])
            if data.get('category'):
                queryset = queryset.filter(category=data['category'])

        if self.search_form.is_valid():
            queryset = self.search_form.search()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        context['search_form'] = self.search_form
        return context