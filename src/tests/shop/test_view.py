from django.test import TestCase
from django.urls import reverse
from shop.models import Product

class TestShopView(TestCase):
    def test_product_list_view(self):
        Product.objects.create(name="Test", price=100)
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")
        print(list(response.context['products']))