from django.test import TestCase
from shop.models import Product, Queue, ProductCategory
from django.core.exceptions import ValidationError

class TestProductModel(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="iPhone 17 Pro Max",
            price=999,
            count_items=500,
            description="Apple",
            is_available=True,
            category=ProductCategory.TECHNIQUE
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "iPhone 17 Pro Max")
        self.assertEqual(self.product.price, 999)
        self.assertEqual(self.product.category, ProductCategory.TECHNIQUE)
        self.assertTrue(self.product.is_available)

    def test_product_str(self):
        self.assertEqual(str(self.product), "iPhone 17 Pro Max")

    def test_zero_count_items_makes_unavailable(self):
        self.product.count_items = 0
        self.product.save()
        self.assertFalse(self.product.is_available) # Не выполнится, т.к. нет установки is_available, в случае count_items == 0