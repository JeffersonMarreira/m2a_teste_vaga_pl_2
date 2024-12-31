from django.db import models
from datetime import datetime, timedelta
import random
import string

class Company(models.Model):
    """
    Model que representa uma Empresa.

    Atributos:
        name (str): O nome da empresa.
        address (str): O endereço da empresa.
        phone (str): O telefone da empresa.
    """

    name = models.CharField("Nome", max_length=255)
    address = models.TextField("Endereço")
    phone = models.CharField("Telefone", max_length=15)

    class Meta:
        """
        Metadados do modelo Company.
        
        Atributos:
            verbose_name (str): Nome singular do modelo.
            verbose_name_plural (str): Nome plural do modelo.
        """
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        """
        Retorna uma string representativa do objeto Company.

        Retorna:
            str: O nome da empresa.
        """
        return self.name


class Employee(models.Model):
    """
    Model que representa um Funcionário.

    Atributos:
        name (str): O nome do funcionário.
        email (str): O e-mail do funcionário, deve ser único.
        company (Company): A empresa à qual o funcionário pertence.
        standard_check_in (datetime.time): Hora padrão de entrada do funcionário.
        standard_check_out (datetime.time): Hora padrão de saída do funcionário.
        auth_code (str): Código de autenticação único do funcionário.
    """

    name = models.CharField("Nome", max_length=255)
    email = models.EmailField("E-mail", unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees", verbose_name="Empresa")
    standard_check_in = models.TimeField("Hora padrão de entrada")
    standard_check_out = models.TimeField("Hora padrão de saída")
    auth_code = models.CharField(max_length=6, unique=True,  editable=False)

    class Meta:
        """
        Metadados do modelo Employee.
        
        Atributos:
            verbose_name (str): Nome singular do modelo.
            verbose_name_plural (str): Nome plural do modelo.
        """
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que um código de autenticação único seja gerado.
        
        Parâmetros:
            *args: Argumentos variáveis.
            **kwargs: Argumentos nomeados variáveis.
        """
        if not self.auth_code:
            self.auth_code = self.generate_unique_auth_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_auth_code():
        """
        Gera um código de autenticação único para o funcionário.

        Retorna:
            str: Um código de 6 dígitos que é único entre todos os funcionários.
        """
        while True:
            code = ''.join(random.choices(string.digits, k=6))
            if not Employee.objects.filter(auth_code=code).exists():
                return code

    def __str__(self):
        """
        Retorna uma string representativa do objeto Employee.

        Retorna:
            str: O nome do funcionário.
        """
        return self.name


class TimeRecord(models.Model):
    """
    Model que representa um Registro de Ponto.

    Atributos:
        employee (Employee): O funcionário relacionado a este registro de ponto.
        date (datetime.date): A data do registro de ponto.
        check_in (datetime.time): Hora de entrada do funcionário (pode ser nulo).
        break_time (datetime.timedelta): Duração do intervalo do funcionário (pode ser nulo).
        check_out (datetime.time): Hora de saída do funcionário (pode ser nulo).
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="time_records", verbose_name="Empresa")
    date = models.DateField("Data")
    check_in = models.TimeField("Entrada", null=True, blank=True)
    break_time = models.DurationField("Intervalo", null=True, blank=True)
    check_out = models.TimeField("Saída", null=True, blank=True)

    class Meta:
        """
        Metadados do modelo TimeRecord.
        
        Atributos:
            verbose_name (str): Nome singular do modelo.
            verbose_name_plural (str): Nome plural do modelo.
        """
        verbose_name = "Registro de Ponto"
        verbose_name_plural = "Registros de Pontos"

    def calculate_worked_hours(self):
        """
        Calcula as horas trabalhadas pelo funcionário, descontando o intervalo.

        Retorna:
            float: Total de horas trabalhadas.
        """
        if self.check_out and self.check_in:
            total_work_time = datetime.combine(self.date, self.check_out) - datetime.combine(self.date, self.check_in)
            break_duration = self.break_time if self.break_time else timedelta()
            return (total_work_time - break_duration).seconds / 3600
        return 0

    def calculate_lateness(self):
        """
        Calcula o tempo de atraso na entrada do funcionário.

        Retorna:
            float: Total de horas de atraso.
        """
        if self.check_in:
            check_in_time = datetime.combine(self.date, self.check_in)
            standard_check_in_time = datetime.combine(self.date, self.employee.standard_check_in)
            if check_in_time > standard_check_in_time:
                return (check_in_time - standard_check_in_time).seconds / 3600
        return 0

    def calculate_overtime(self):
        """
        Calcula o tempo de horas extras do funcionário.

        Retorna:
            float: Total de horas extras.
        """
        if self.check_out:
            check_out_time = datetime.combine(self.date, self.check_out)
            standard_check_out_time = datetime.combine(self.date, self.employee.standard_check_out)
            if check_out_time > standard_check_out_time:
                return (check_out_time - standard_check_out_time).seconds / 3600
        return 0

    def __str__(self):
        """
        Retorna uma string representativa do objeto TimeRecord.

        Retorna:
            str: String representativa do registro de ponto.
        """
        return f"Ponto de {self.employee.name} em {self.date}"
