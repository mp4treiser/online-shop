from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Product, ProductCategory
from .models.forms import ProductForm, ProductFilterForm, ProductSearchForm

from .tasks import debug_task


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        debug_task.delay(1)
        context['categories'] = ProductCategory.choices
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']  # Сортировка по ID в обратном порядке (новые сначала)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        debug_task.delay(1)
        context['filter_form'] = ProductFilterForm(self.request.GET)
        context['search_form'] = ProductSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-id')  # Базовая сортировка
        filter_form = ProductFilterForm(self.request.GET)
        search_form = ProductSearchForm(self.request.GET)

        if filter_form.is_valid():
            min_price = filter_form.cleaned_data.get('min_price')
            max_price = filter_form.cleaned_data.get('max_price')
            category = filter_form.cleaned_data.get('category')

            if min_price is not None:
                queryset = queryset.filter(price__gte=float(min_price))
            if max_price is not None:
                queryset = queryset.filter(price__lte=float(max_price))
            if category:
                queryset = queryset.filter(category=category)

        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(description__icontains=query)
                )

        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/category.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context

class InfoView(TemplateView):
    template_name = 'info.html'