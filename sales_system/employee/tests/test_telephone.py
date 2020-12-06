from rest_framework.test import APITestCase
from rest_framework import status
from employee.models import (
    Employee,
    Telephone
)


class TelephoneRetrieveListTests(APITestCase):
    url = '/apiV1/telephone/'

    def setUp(self):
        Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515151
        )
        Telephone.objects.create(
            country_code='+55',
            region_code='0222',
            number=151515152
        )

    def test_telephone_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'country_code', count=2)
        self.assertContains(response, 'region_code', count=2)
        self.assertContains(response, 'number', count=2)

    def test_telephone_retrieve(self):
        telephone = Telephone.objects.first()
        response = self.client.get(self.url + str(telephone.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'country_code', count=1)
        self.assertContains(response, 'region_code', count=1)
        self.assertContains(response, 'number', count=1)


class TelephoneCreateTests(APITestCase):
    url = '/apiV1/telephone/'

    def test_telephone_all_attributes(self):
        data = {
            'country_code': '+54',
            'region_code': '0221',
            'number': 151515151
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Telephone.objects.count(), 1)
        self.assertEqual(Telephone.objects.get().number, 151515151)

    def test_telephone_without_country_code(self):
        data = {
            'region_code': '0221',
            'number': 151515151
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_telephone_without_region_code(self):
        data = {
            'country_code': '+54',
            'number': 151515151
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_telephone_without_number(self):
        data = {
            'country_code': '+54',
            'region_code': '0221'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_telephones_equals(self):
        data = {
            'country_code': '+54',
            'region_code': '0221',
            'number': 151515151
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TelephoneUpdateTests(APITestCase):
    url = '/apiV1/telephone/'

    def setUp(self):
        Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515151
        )
        Telephone.objects.create(
            country_code='+55',
            region_code='0222',
            number=151515152
        )

    def test_telephone(self):
        telephone = Telephone.objects.first()
        data = {
            'country_code': '+56',
            'region_code': '0222',
            'number': 151515154
        }
        url = self.url + str(telephone.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'country_code', count=1)
        self.assertContains(response, 'region_code', count=1)
        self.assertContains(response, 'number', count=1)
        self.assertEqual(response.data['country_code'], '+56')
        self.assertEqual(response.data['region_code'], '0222')
        self.assertEqual(response.data['number'], 151515154)

    def test_telephone_without_country_code(self):
        telephone = Telephone.objects.first()
        data = {
            'region_code': '0222',
            'number': 151515154
        }
        url = self.url + str(telephone.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_telephone_without_region_code(self):
        telephone = Telephone.objects.first()
        data = {
            'country_code': '0222',
            'number': 151515154
        }
        url = self.url + str(telephone.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_telephone_without_number(self):
        telephone = Telephone.objects.first()
        data = {
            'country_code': '0222',
            'region_code': '0221'
        }
        url = self.url + str(telephone.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TelephoneDeleteTests(APITestCase):
    url = '/apiV1/telephone/'

    def setUp(self):
        t1 = Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515151
        )
        Telephone.objects.create(
            country_code='+55',
            region_code='0222',
            number=151515152
        )
        Employee.objects.create(
            first_name='Juan1',
            second_name='Perez1',
            surname='Juan2',
            second_surname='Perez1',
            number=1,
            birthdate='1979-01-01',
            date_of_admission='1999-01-01',
            email='Email@Email.com',
            reference='Reference',
            sector='A',
            active=True,
            telephone=t1
        )

    def test_telephone_with_employee(self):
        telephone = Telephone.objects.get(number=151515151)
        url = self.url + str(telephone.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Telephone.objects.count(), 2)

    def test_telephone_without_employee(self):
        telephone = Telephone.objects.get(number=151515152)
        url = self.url + str(telephone.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Telephone.objects.count(), 1)

    def test_telephone_bad_id(self):
        url = self.url + '400/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Telephone.objects.count(), 2)
