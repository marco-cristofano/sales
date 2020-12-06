from rest_framework.test import APITestCase
from rest_framework import status
from product.models import (
    Brand,
    Product
)


class BrandAndProductTests(APITestCase):
    url = '/apiV1/brand_and_product/'

    def setUp(self):
        b1 = Brand.objects.create(
            country='country',
            name='marca',
            address='address'
        )
        b2 = Brand.objects.create(
            country='country1',
            name='marca1',
            address='address1'
        )
        Product.objects.create(
            description='descripcion',
            weight=100,
            stock=100,
            price=100,
            brand=b1
        )
        Product.objects.create(
            description='descripcion1',
            weight=101,
            stock=101,
            price=101,
            brand=b2
        )

    def test_brand_and_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'country', count=4)
        self.assertContains(response, 'name', count=2)
        self.assertContains(response, 'address', count=4)
        self.assertContains(response, 'description', count=2)
        self.assertContains(response, 'weight', count=2)
        self.assertContains(response, 'stock', count=2)
        self.assertContains(response, 'price', count=2)
        self.assertContains(response, 'brand', 2)

    def test_telephone_create(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_telephone_put(self):
        product = Product.objects.first()
        url = self.url + str(product.pk) + '/'
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_telephone_delete(self):
        product = Product.objects.first()
        url = self.url + str(product.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
