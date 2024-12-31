from django.test import TestCase
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
