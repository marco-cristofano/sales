from rest_framework.test import APITestCase
from rest_framework import status
from employee.models import (
    Employee,
    Telephone
)


class EployeeBasicTests(APITestCase):
    url = '/apiV1/employee/'

    def setUp(self):
        t1 = Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515151
        )
        t2 = Telephone.objects.create(
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
            telephone=t2
        )

    def test_telephone_list(self):
        response = self.client.get(self.url + 'basic/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'first_name', count=2)
        self.assertContains(response, 'surname', count=2)
        self.assertContains(response, 'email', count=2)
        self.assertContains(response, 'number', count=2)

    def test_telephone_retrieve(self):
        employee = Employee.objects.first()
        url = self.url + str(employee.pk) + '/basic/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertContains(response, 'first_name', count=1)
        self.assertContains(response, 'surname', count=1)
        self.assertContains(response, 'email', count=1)
        self.assertContains(response, 'number', count=1)

    def test_telephone_create(self):
        response = self.client.post(self.url + 'basic/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_telephone_put(self):
        employee = Employee.objects.first()
        url = self.url + str(employee.pk) + '/basic/'
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_telephone_delete(self):
        employee = Employee.objects.first()
        url = self.url + str(employee.pk) + '/basic/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
