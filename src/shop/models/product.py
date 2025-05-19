from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError('Цена должна быть больше нуля')

class ProductCategory(models.TextChoices):
    TECHNIQUE = "TQ", _("Technique")
    BOOK = "BK", _("Book")
    FURNITURE = "FR", _("Furniture")
    SPORT = "SP", _("Sport")
    CHILDREN = "CN", _("Children")
    DEFAULT = "DF", _("Default")

class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name="Наименование продукта")
    description = models.CharField(max_length=200,null=True, blank=True, verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена", validators=[validate_positive_price])
    is_available = models.BooleanField(default=True, verbose_name="Доступен к продаже")
    category = models.CharField(
         choices=ProductCategory,
         default=ProductCategory.DEFAULT,
         verbose_name="Категория продукта"
    )
    rating = models.FloatField(null=True,blank=True, verbose_name="Рейтинг")
    photo = models.ImageField(upload_to="products/%Y/%m/%d/", null=True,blank=True, verbose_name="Фото")
    def image_preview(self):
        if self.photo:
            return format_html(
                '<img src="{}" width="150" />',
                 self.photo.url  # Используем URL изображения
        )
        return ""
    image_preview.short_description = 'Превью'
    count_items = models.IntegerField(default=10, verbose_name="Количество")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    provider = models.ForeignKey(
        to="Provider",
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
        verbose_name="Производитель"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )

    def __str__(self):
        return f"{self.name}"