from import_export import resources, fields
from import_export.widgets import DecimalWidget
from .models import Company, Employee, TimeRecord

class CompanyResource(resources.ModelResource):
    """
    Recurso de importação/exportação para o modelo Company.

    Campos:
        Nome (str): Nome da empresa.
        Endereço (str): Endereço da empresa.
        Telefone (str): Telefone da empresa.
    """
    
    Nome = fields.Field(column_name='name', attribute='name')
    Endereço = fields.Field(column_name='address', attribute='address')
    Telefone = fields.Field(column_name='phone', attribute='phone')

    class Meta:
        """
        Metadados do recurso CompanyResource.

        Campos:
            model (Model): O modelo associado ao recurso.
            fields (tuple): Os campos a serem exportados/importados.
        """
        model = Company
        fields = ('id', 'name', 'address', 'phone')


class EmployeeResource(resources.ModelResource):
    """
    Recurso de importação/exportação para o modelo Employee.

    Campos:
        name (str): Nome do funcionário.
        email (str): E-mail do funcionário.
        company__id (int): ID da empresa à qual o funcionário pertence.
        company__name (str): Nome da empresa à qual o funcionário pertence.
        standard_check_in (datetime.time): Hora padrão de entrada.
        standard_check_out (datetime.time): Hora padrão de saída.
    """
    
    name = fields.Field(column_name='Nome', attribute='name')
    email = fields.Field(column_name='E-mail', attribute='email')
    company__id = fields.Field(column_name='ID da Empresa', attribute='company__id')
    company__name = fields.Field(column_name='Nome da Empresa', attribute='company__name')
    standard_check_in = fields.Field(column_name='Hora Padrão de Entrada', attribute='standard_check_in')
    standard_check_out = fields.Field(column_name='Hora Padrão de Saída', attribute='standard_check_out')

    class Meta:
        """
        Metadados do recurso EmployeeResource.

        Campos:
            model (Model): O modelo associado ao recurso.
            fields (tuple): Os campos a serem exportados/importados.
        """
        model = Employee
        fields = ('id', 'name', 'email', 'company__id','company__name', 'standard_check_in', 'standard_check_out')


class TimeRecordResource(resources.ModelResource):
    """
    Recurso de importação/exportação para o modelo TimeRecord.

    Campos:
        employee__id (int): ID do funcionário associado ao registro de ponto.
        employee__name (str): Nome do funcionário associado ao registro de ponto.
        date (datetime.date): Data do registro de ponto.
        check_in (datetime.time): Hora de entrada.
        break_time (datetime.timedelta): Duração do intervalo.
        check_out (datetime.time): Hora de saída.
        worked_hours (float): Horas trabalhadas calculadas.
        lateness (float): Tempo de atraso calculado.
        overtime (float): Tempo de horas extras calculado.
    """
    
    employee__id = fields.Field(column_name='ID do Funcionário', attribute='employee__id')
    employee__name = fields.Field(column_name='Nome do Funcionário', attribute='employee__name')
    date = fields.Field(column_name='Data', attribute='date')
    check_in = fields.Field(column_name='Entrada', attribute='check_in')
    break_time = fields.Field(column_name='Intervalo', attribute='break_time')
    check_out = fields.Field(column_name='Saída', attribute='check_out')
    worked_hours = fields.Field(column_name='Horas Trabalhadas', attribute='worked_hours', widget=DecimalWidget())
    lateness = fields.Field(column_name='Atraso', attribute='lateness', widget=DecimalWidget())
    overtime = fields.Field(column_name='Horas Extras', attribute='overtime', widget=DecimalWidget())

    class Meta:
        """
        Metadados do recurso TimeRecordResource.

        Campos:
            model (Model): O modelo associado ao recurso.
            fields (tuple): Os campos a serem exportados/importados.
        """
        model = TimeRecord
        fields = ('id', 'employee__id', 'employee__name', 'date', 'check_in', 'break_time', 'check_out', 'worked_hours', 'lateness', 'overtime')

    def dehydrate_worked_hours(self, record):
        """
        Calcula e formata as horas trabalhadas para exportação.

        Parâmetros:
            record (TimeRecord): O registro de ponto.

        Retorna:
            float: Total de horas trabalhadas.
        """
        return round(record.calculate_worked_hours(), 2)

    def dehydrate_lateness(self, record):
        """
        Calcula e formata o tempo de atraso para exportação.

        Parâmetros:
            record (TimeRecord): O registro de ponto.

        Retorna:
            float: Total de horas de atraso.
        """
        return round(record.calculate_lateness(), 2)

    def dehydrate_overtime(self, record):
        """
        Calcula e formata as horas extras para exportação.

        Parâmetros:
            record (TimeRecord): O registro de ponto.

        Retorna:
            float: Total de horas extras.
        """
        return round(record.calculate_overtime(), 2)
