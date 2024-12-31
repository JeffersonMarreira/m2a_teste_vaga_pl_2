from django.db import models
from datetime import datetime, timedelta
import random
import string

class Company(models.Model):
    name = models.CharField("Nome", max_length=255)
    address = models.TextField("Endereço")
    phone = models.CharField("Telefone", max_length=15)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField("Nome", max_length=255)
    email = models.EmailField("E-mail", unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees", verbose_name="Empresa")
    standard_check_in = models.TimeField("Hora padrão de entrada")
    standard_check_out = models.TimeField("Hora padrão de saída")
    auth_code = models.CharField(max_length=6, unique=True,  editable=False)


    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def save(self, *args, **kwargs):
        # Gera um código único apenas se o auth_code estiver vazio
        if not self.auth_code:
            self.auth_code = self.generate_unique_auth_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_auth_code():
        # Gera um código aleatório e verifica se já existe
        while True:
            code = ''.join(random.choices(string.digits, k=6))
            if not Employee.objects.filter(auth_code=code).exists():
                return code

    def __str__(self):
        return self.name

class TimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="time_records", verbose_name="Empresa")
    date = models.DateField("Data")
    check_in = models.TimeField("Entrada", null=True, blank=True)
    break_time = models.DurationField("Intervalo", null=True, blank=True)
    check_out = models.TimeField("Saída", null=True, blank=True)

    class Meta:
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Pontos"

    def calculate_worked_hours(self):
        if self.check_out and self.check_in:
            total_work_time = datetime.combine(self.date, self.check_out) - datetime.combine(self.date, self.check_in)
            break_duration = self.break_time if self.break_time else timedelta()
            return (total_work_time - break_duration).seconds / 3600
        return 0

    def calculate_lateness(self):
        if self.check_in:
            check_in_time = datetime.combine(self.date, self.check_in)
            standard_check_in_time = datetime.combine(self.date, self.employee.standard_check_in)
            if check_in_time > standard_check_in_time:
                return (check_in_time - standard_check_in_time).seconds / 3600
        return 0

    def calculate_overtime(self):
        if self.check_out:
            check_out_time = datetime.combine(self.date, self.check_out)
            standard_check_out_time = datetime.combine(self.date, self.employee.standard_check_out)
            if check_out_time > standard_check_out_time:
                return (check_out_time - standard_check_out_time).seconds / 3600
        return 0

    def __str__(self):
        return f"Ponto de {self.employee.name} em {self.date}"



