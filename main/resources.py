from import_export import resources, fields
from import_export.widgets import DecimalWidget
from .models import Company, Employee, TimeRecord

class CompanyResource(resources.ModelResource):
    Nome = fields.Field(column_name='name', attribute='name')
    Endereço = fields.Field(column_name='address', attribute='address')
    Telefone = fields.Field(column_name='phone', attribute='phone')

    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'phone')

class EmployeeResource(resources.ModelResource):
    name = fields.Field(column_name='Nome', attribute='name')
    email = fields.Field(column_name='E-mail', attribute='email')
    company__id = fields.Field(column_name='ID da Empresa', attribute='company__id')
    company__name = fields.Field(column_name='Nome da Empresa', attribute='company__name')
    standard_check_in = fields.Field(column_name='Hora Padrão de Entrada', attribute='standard_check_in')
    standard_check_out = fields.Field(column_name='Hora Padrão de Saída', attribute='standard_check_out')

    class Meta:
        model = Employee
        fields = ('id', 'name', 'email', 'company__id','company__name', 'standard_check_in', 'standard_check_out')

class TimeRecordResource(resources.ModelResource):
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
        model = TimeRecord
        fields = ('id', 'employee__id', 'employee__name','date', 'check_in', 'break_time', 'check_out', 'worked_hours', 'lateness', 'overtime')

    def dehydrate_worked_hours(self, record):
        return round(record.calculate_worked_hours(), 2)

    def dehydrate_lateness(self, record):
        return round(record.calculate_lateness(), 2)

    def dehydrate_overtime(self, record):
        return round(record.calculate_overtime(), 2)

