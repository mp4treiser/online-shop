from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from ..models import (
    Product,
    Order,
    ProductDetail,
    Provider,
    ProductOrder,
    Feedback, ProviderRating
)
from ..models.base import Rating
from ..models.product_rating import ProductRating


class ProviderProductInline(admin.TabularInline):
    model = Product
    extra = 1

class ProviderAdmin(admin.ModelAdmin):
    inlines = [
        ProviderProductInline
    ]

@admin.action(description="Mark selected as unavailable")
def mark_as_unavailable(modeladmin, request, queryset):
    queryset.update(is_available=False)

class ProductAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    readonly_fields = ['image_preview']
    actions = [mark_as_unavailable]

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'price', 'count_items', 'is_available','rating'),  # Замените на ваши поля
            'description': 'Основные сведения о товаре'
        }),
        ('Фото и описание', {
            'fields': ('image_preview', 'photo', 'description'),
            'description': 'Изображения и детальное описание'
        }),
        ('Поставщик', {
            'fields': ('provider',),
            'description': 'Информация о поставщике'
        }),
    )
    list_display = ("name", "price", "is_available", "category","count_items")
    list_filter = ("category","is_available","provider")
    search_fields = ("name","description")
    list_display_links = ("name","category")
    list_editable = ("price","is_available")
    list_per_page = 5

product_admin = admin.site.register(Product, ProductAdmin)
provider_admin = admin.site.register(Provider, ProviderAdmin)
admin.site.register(Order)
admin.site.register(ProductDetail)
admin.site.register(ProductOrder)
admin.site.register(Feedback)
admin.site.register(Rating)
admin.site.register(ProductRating)
admin.site.register(ProviderRating)