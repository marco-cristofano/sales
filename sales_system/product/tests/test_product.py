from rest_framework.test import APITestCase
from rest_framework import status
from product.models import (
    Brand,
    Product
)


class EjemploFixtureBrandTest(APITestCase):
    url = '/apiV1/brand/'
    fixtures = [
        'product/fixtures/product.json',
    ]

    def test_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ProductRetrieveListTests(APITestCase):
    url = '/apiV1/product/'

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

    def test_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'description', count=2)
        self.assertContains(response, 'weight', count=2)
        self.assertContains(response, 'stock', count=2)
        self.assertContains(response, 'price', count=2)
        self.assertContains(response, 'brand', count=2)

    def test_product_retrieve(self):
        product = Product.objects.first()
        response = self.client.get(self.url + str(product.pk) + '/')
        self.assertContains(response, 'description', count=1)
        self.assertContains(response, 'weight', count=1)
        self.assertContains(response, 'stock', count=1)
        self.assertContains(response, 'price', count=1)
        self.assertContains(response, 'brand', count=1)


class ProductCreateTests(APITestCase):
    url = '/apiV1/product/'

    def setUp(self):
        Brand.objects.create(
            country='pais',
            name='marca',
            address='address'
        )

    def test_product_all_attributes(self):
        b1 = Brand.objects.get(country='pais')
        data = {
            'description': 'descripcion',
            'weight': 100,
            'stock': 100,
            'price': 100,
            'brand': b1.pk,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().description, 'descripcion')

    def test_product_single_required_attributes(self):
        b1 = Brand.objects.get(country='pais')
        data = {
            'description': 'descripcion1',
            'stock': 100,
            'price': 100,
            'brand': b1.pk,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_without_required_atrributes(self):
        b1 = Brand.objects.get(country='pais')
        for atrr in ('description', 'stock', 'price', 'brand'):
            data = {
                'description': 'descripcion1',
                'stock': 100,
                'price': 100,
                'brand': b1.pk,
            }
            data.pop(atrr)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductUpdateTests(APITestCase):
    url = '/apiV1/product/'

    def setUp(self):
        b1 = Brand.objects.create(
            country='country',
            name='marca',
            address='address'
        )
        Product.objects.create(
            description='descripcion',
            weight=100,
            stock=100,
            price=100,
            brand=b1
        )

    def test_product(self):
        b1 = Product.objects.get(description='descripcion')
        product = Product.objects.first()
        data = {
            'description': 'descripcion1',
            'stock': 101,
            'price': 101,
            'brand': b1.pk,
        }
        url = self.url + str(product.pk) + '/'
        response = self.client.put(url, data)
        self.assertContains(response, 'description', count=1)
        self.assertContains(response, 'weight', count=1)
        self.assertContains(response, 'stock', count=1)
        self.assertContains(response, 'price', count=1)
        self.assertContains(response, 'brand', count=1)
        self.assertEqual(response.data['description'], 'descripcion1')
        self.assertEqual(response.data['weight'], '100.000')
        self.assertEqual(response.data['stock'], 101)
        self.assertEqual(response.data['price'], '101.000')

    def test_without_required_attributes(self):
        b1 = Product.objects.get(description='descripcion')
        product = Product.objects.first()
        for atrr in ('description', 'stock', 'price', 'brand'):
            data = {
                'description': 'descripcion1',
                'stock': 100,
                'price': 100,
                'brand': b1.pk,
            }
            data.pop(atrr)
            url = self.url + str(product.pk) + '/'
            response = self.client.put(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductDeleteTests(APITestCase):
    url = '/apiV1/product/'

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

    def test_product(self):
        product = Product.objects.first()
        url = self.url + str(product.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_product_bad_id(self):
        url = self.url + '400/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.count(), 2)
