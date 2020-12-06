from rest_framework.test import APITestCase
from rest_framework import status
from employee.models import (
    Employee,
    Telephone
)


class EployeeRetrieveListTests(APITestCase):
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertContains(response, 'first_name', count=2)
        self.assertContains(response, 'second_name', count=2)
        self.assertContains(response, 'surname', count=4)
        self.assertContains(response, 'second_surname', count=2)
        self.assertContains(response, 'birthdate', count=2)
        self.assertContains(response, 'date_of_admission', count=2)
        self.assertContains(response, 'email', count=2)
        self.assertContains(response, 'reference', count=2)
        self.assertContains(response, 'sector', count=2)
        self.assertContains(response, 'active', count=2)
        self.assertContains(response, 'telephone', count=2)

    def test_telephone_retrieve(self):
        telephone = Employee.objects.first()
        response = self.client.get(self.url + str(telephone.pk) + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'first_name', count=1)
        self.assertContains(response, 'second_name', count=1)
        self.assertContains(response, 'surname', count=2)
        self.assertContains(response, 'second_surname', count=1)
        self.assertContains(response, 'birthdate', count=1)
        self.assertContains(response, 'date_of_admission', count=1)
        self.assertContains(response, 'email', count=1)
        self.assertContains(response, 'reference', count=1)
        self.assertContains(response, 'sector', count=1)
        self.assertContains(response, 'active', count=1)
        self.assertContains(response, 'telephone', count=1)


class EmployeeCreateTests(APITestCase):
    url = '/apiV1/employee/'

    def setUp(self):
        Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515151
        )
        Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515152
        )

    def test_employee_all_attributes(self):
        t1 = Telephone.objects.get(number=151515151)
        data = {
            'first_name': 'Juan1',
            'second_name': 'Perez1',
            'surname': 'Juan2',
            'second_surname': 'Perez1',
            'number': 1,
            'birthdate': '1979-01-01',
            'date_of_admission': '1999-01-01',
            'email': 'Email@Email.com',
            'reference': 'Reference',
            'sector': 'A',
            'active': True,
            'telephone': t1.pk
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().first_name, 'Juan1')

    def test_employee_single_required_attributes(self):
        t1 = Telephone.objects.get(number=151515152)
        data = {
            'first_name': 'Juan1',
            'surname': 'Juan2',
            'second_surname': 'Perez1',
            'number': 1,
            'date_of_admission': '1999-01-01',
            'email': 'Email@Email.com',
            'sector': 'A',
            'active': True,
            'telephone': t1.pk
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().first_name, 'Juan1')

    def test_employee_birthdate_gt_date_of_admission(self):
        t1 = Telephone.objects.get(number=151515152)
        data = {
            'first_name': 'Juan1',
            'second_name': 'Perez1',
            'surname': 'Juan2',
            'second_surname': 'Perez1',
            'number': 1,
            'birthdate': '2000-01-01',
            'date_of_admission': '1999-01-01',
            'email': 'Email@Email.com',
            'reference': 'Reference',
            'sector': 'A',
            'active': True,
            'telephone': t1.pk
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_without_required_atrributes(self):
        t1 = Telephone.objects.get(number=151515152)
        for atrr in ('first_name', 'surname', 'second_surname',
                     'number', 'date_of_admission', 'email', 'sector',
                     'active', 'telephone'):
            data = {
                'first_name': 'Juan1',
                'surname': 'Juan2',
                'second_surname': 'Perez1',
                'number': 1,
                'date_of_admission': '1999-01-01',
                'email': 'Email@Email.com',
                'sector': 'A',
                'active': True,
                'telephone': t1.pk
            }
            data.pop(atrr)
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmployeeUpdateTests(APITestCase):
    url = '/apiV1/employee/'

    def setUp(self):
        t1 = Telephone.objects.create(
            country_code='+54',
            region_code='0221',
            number=151515151
        )
        Employee.objects.create(
            first_name='Juan1',
            second_name='Juan1',
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

    def test_employee(self):
        t1 = Telephone.objects.get(number=151515151)
        employee = Employee.objects.first()
        data = {
            'first_name': 'Juan3',
            'surname': 'Perez3',
            'second_surname': 'Perez3',
            'number': 3,
            'date_of_admission': '1990-01-01',
            'email': 'Email1@Email.com',
            'sector': 'B',
            'active': False,
            'telephone': t1.pk
        }
        url = self.url + str(employee.pk) + '/'
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'first_name', count=1)
        self.assertContains(response, 'second_name', count=1)
        self.assertContains(response, 'surname', count=2)
        self.assertContains(response, 'second_surname', count=1)
        self.assertContains(response, 'birthdate', count=1)
        self.assertContains(response, 'date_of_admission', count=1)
        self.assertContains(response, 'email', count=1)
        self.assertContains(response, 'reference', count=1)
        self.assertContains(response, 'sector', count=1)
        self.assertContains(response, 'active', count=1)
        self.assertContains(response, 'telephone', count=1)
        self.assertEqual(response.data['first_name'], 'Juan3')
        self.assertEqual(response.data['second_name'], 'Juan1')
        self.assertEqual(response.data['surname'], 'Perez3')
        self.assertEqual(response.data['second_surname'], 'Perez3')
        self.assertEqual(response.data['birthdate'], '1979-01-01')
        self.assertEqual(response.data['date_of_admission'], '1990-01-01')
        self.assertEqual(response.data['email'], 'Email1@Email.com')
        self.assertEqual(response.data['reference'], 'Reference')
        self.assertEqual(response.data['sector'], 'B')
        self.assertEqual(response.data['active'], False)
        self.assertEqual(response.data['telephone'], t1.pk)

    def test_without_required_attributes(self):
        t1 = Telephone.objects.get(number=151515151)
        employee = Employee.objects.first()
        for atrr in ('first_name', 'surname', 'second_surname', 'number',
                     'date_of_admission', 'email', 'sector', 'telephone'):
            data = {
                'first_name': 'Juan3',
                'surname': 'Perez3',
                'second_surname': 'Perez3',
                'number': 3,
                'date_of_admission': '1990-01-01',
                'email': 'Email1@Email.com',
                'sector': 'B',
                'active': False,
                'telephone': t1.pk
            }
            data.pop(atrr)
            url = self.url + str(employee.pk) + '/'
            response = self.client.put(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EmployeeDeleteTests(APITestCase):
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

    def test_employee(self):
        telephone = Employee.objects.first()
        url = self.url + str(telephone.pk) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 1)

    def test_telephone_bad_id(self):
        url = self.url + '400/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Employee.objects.count(), 2)
