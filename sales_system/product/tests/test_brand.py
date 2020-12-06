from rest_framework.test import APITestCase
from rest_framework import status
from product.models import (
    Brand,
    Product
)


class BrandRetrieveListTests(APITestCase):
    url = '/apiV1/brand/'

    def setUp(self):
        Brand.objects.create(
            country='country',
            name='marca',
            address='address'
        )
        Brand.objects.create(
            country='country1',
            name='marca1',
            address='address1'
        )

    def test_telephone_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'country', count=4)
        self.assertContains(response, 'name', count=2)
        self.assertContains(response, 'address', count=4)

    def test_telephone_retrieve(self):
        brand = Brand.objects.first()
        response = self.client.get(self.url + str(brand.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'country', count=2)
        self.assertContains(response, 'name', count=1)
        self.assertContains(response, 'address', count=2)


class BrandCreateTests(APITestCase):
    url = '/apiV1/brand/'

    def test_employee_all_attributes(self):
        data = {
            'country': 'Argentina',
            'name': 'Marca',
            'address': 'bsas'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(Brand.objects.get().name, 'Marca')

    def test_employee_without_country(self):
        data = {
            'name': 'Marca',
            'address': 'bsas'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_employee_without_region_code(self):
        data = {
            'country': '+54',
            'address': '151515151'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_without_number(self):
        data = {
            'name': '+54',
            'country': '0221'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BrandUpdateTests(APITestCase):
    url = '/apiV1/brand/'

    def setUp(self):
        Brand.objects.create(
            country='country',
            name='marca',
            address='address'
        )
        Brand.objects.create(
            country='country1',
            name='marca1',
            address='address1'
        )

    def test_brand(self):
        brand = Brand.objects.first()
        data = {
            'name': 'Marca',
            'country': 'Pais',
            'address': 'Dir'
        }
        url = self.url + str(brand.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'name', count=1)
        self.assertContains(response, 'country', count=1)
        self.assertContains(response, 'address', count=1)
        self.assertEqual(response.data['name'], 'Marca')
        self.assertEqual(response.data['country'], 'Pais')
        self.assertEqual(response.data['address'], 'Dir')

    def test_brand_without_country(self):
        brand = Brand.objects.first()
        data = {
            'name': '0222',
            'address': '151515154'
        }
        url = self.url + str(brand.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_brand_without_region_name(self):
        brand = Brand.objects.first()
        data = {
            'country': '0222',
            'address': '151515154'
        }
        url = self.url + str(brand.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_brand_without_address(self):
        brand = Brand.objects.first()
        data = {
            'name': '0222',
            'country': '0221'
        }
        url = self.url + str(brand.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BrandDeleteTests(APITestCase):
    url = '/apiV1/brand/'

    def setUp(self):
        b1 = Brand.objects.create(
            country='country',
            name='marca',
            address='address'
        )
        Brand.objects.create(
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

    def test_brand_with_employee(self):
        brand = Brand.objects.get(name='marca')
        url = self.url + str(brand.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Brand.objects.count(), 2)

    def test_brand_without_employee(self):
        brand = Brand.objects.get(name='marca1')
        url = self.url + str(brand.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Brand.objects.count(), 1)

    def test_brand_bad_id(self):
        url = self.url + '400/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Brand.objects.count(), 2)
