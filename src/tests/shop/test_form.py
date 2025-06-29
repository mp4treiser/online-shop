from django.test import TestCase
from shop.models.forms import ProductForm
from shop.models import Product, ProductCategory

class TestProductForm(TestCase):
    def test_valid_form(self):
        form_data = {
            "name": "Test Product",
            "price": 100,
            "count_items": 10,
            "category": ProductCategory.TECHNIQUE,
            "is_available": True,
            "description": "Test description",
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_price(self):
        # Тест на валидацию цены
        form_data = {
            "name": "Test Product",
            "price": 0,  # Невалидная цена, пройдёт, т.к. нет валидации на то, что не может быть равно 0
            "category": ProductCategory.TECHNIQUE,
            "count_items": 10,
            "is_available": True,
            "description": "Test description",
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_zero_count_but_available(self):
        # Тест на проверку, что товар не может быть доступен при нулевом количестве
        form_data = {
            "name": "Test Product",
            "price": 100,
            "category": ProductCategory.TECHNIQUE,
            "count_items": 0, # Ошибки не будет, т.к. is_available = True и count_items = 0 не связаны
            "is_available": True,
            "description": "Test description",
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
