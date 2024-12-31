from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Company, Employee, TimeRecord
from datetime import datetime, time

class CompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")

    def test_company_str(self):
        self.assertEqual(str(self.company), self.company.name)

class EmployeeModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")
        self.employee = Employee.objects.create(
            name="Funcionário Teste",
            email="teste@empresa.com",
            company=self.company,
            standard_check_in=time(9, 0),
            standard_check_out=time(18, 0)
        )

    def test_employee_str(self):
        self.assertEqual(str(self.employee), self.employee.name)

    def test_auth_code_generated(self):
        self.assertTrue(self.employee.auth_code)

class TimeRecordModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")
        self.employee = Employee.objects.create(
            name="Funcionário Teste",
            email="teste@empresa.com",
            company=self.company,
            standard_check_in=time(9, 0),
            standard_check_out=time(18, 0)
        )
        self.time_record = TimeRecord.objects.create(
            employee=self.employee,
            date=datetime.today().date(),
            check_in=time(9, 0),
            check_out=time(18, 0)
        )

    def test_time_record_str(self):
        self.assertEqual(str(self.time_record), f"Ponto de {self.employee.name} em {self.time_record.date}")

    def test_calculate_worked_hours(self):
        self.assertEqual(self.time_record.calculate_worked_hours(), 9.0)

    def test_calculate_lateness(self):
        self.time_record.check_in = time(9, 30)
        self.time_record.save()
        self.assertEqual(self.time_record.calculate_lateness(), 0.5)

    def test_calculate_overtime(self):
        self.time_record.check_out = time(19, 0)
        self.time_record.save()
        self.assertEqual(self.time_record.calculate_overtime(), 1.0)


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")
        self.employee = Employee.objects.create(
            name="Funcionário Teste",
            email="teste@empresa.com",
            company=self.company,
            standard_check_in=time(9, 0),
            standard_check_out=time(18, 0),
            auth_code="123456"
        )

    def test_home_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_post_check_in(self):
        response = self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'check_in'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ação check_in concluída para Funcionário Teste")

    def test_home_post_invalid_auth_code(self):
        response = self.client.post(reverse('home'), {
            'auth_code': 'invalid_code',
            'action': 'check_in'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.context['message'], "Ocorreu um erro: No Employee matches the given query.")

    def test_home_post_start_break(self):
        self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'check_in'
        })
        response = self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'start_break'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ação start_break concluída para Funcionário Teste")

    def test_home_post_end_break(self):
        self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'check_in'
        })
        self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'start_break'
        })
        response = self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'end_break'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ação end_break concluída para Funcionário Teste")

    def test_home_post_check_out(self):
        self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'check_in'
        })
        response = self.client.post(reverse('home'), {
            'auth_code': self.employee.auth_code,
            'action': 'check_out'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ação check_out concluída para Funcionário Teste")


class CompanyAPITest(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")
        self.company_url = reverse('company-list')

    def test_get_companies(self):
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_company(self):
        data = {"name": "Nova Empresa", "address": "Novo Endereço", "phone": "987654321"}
        response = self.client.post('/api/companies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)

class EmployeeAPITest(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")
        self.employee = Employee.objects.create(
            name="Funcionário Teste",
            email="teste@empresa.com",
            company=self.company,
            standard_check_in=time(9, 0),
            standard_check_out=time(18, 0),
            auth_code="123456"
        )
        self.employee_url = reverse('employee-list')

    def test_get_employees(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_employee(self):
        data = {
            "name": "Novo Funcionário",
            "email": "novo@empresa.com",
            "company": self.company.id,
            "standard_check_in": "09:00:00",
            "standard_check_out": "18:00:00"
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

class TimeRecordAPITest(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Empresa Teste", address="Endereço Teste", phone="123456789")
        self.employee = Employee.objects.create(
            name="Funcionário Teste",
            email="teste@empresa.com",
            company=self.company,
            standard_check_in=time(9, 0),
            standard_check_out=time(18, 0),
            auth_code="123456"
        )
        self.time_record = TimeRecord.objects.create(
            employee=self.employee,
            date=datetime.today().date(),
            check_in=time(9, 0),
            check_out=time(18, 0)
        )
        self.time_record_url = reverse('timerecord-list')

    def test_get_time_records(self):
        response = self.client.get('/api/time-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_time_record(self):
        data = {
            "employee": self.employee.id,
            "date": datetime.today().date(),
            "check_in": "09:00:00",
            "check_out": "18:00:00"
        }
        response = self.client.post('/api/time-records/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TimeRecord.objects.count(), 2)
