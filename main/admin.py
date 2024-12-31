from django.contrib import admin
from .models import Company, Employee, TimeRecord
from import_export.admin import ExportActionMixin
from .resources import CompanyResource, EmployeeResource, TimeRecordResource
from import_export.formats.base_formats import XLSX
from .pdf_format import PDF

"""
Configuração do Admin para o modelo Company.
Esta classe personaliza a interface de administração para o modelo Company, incluindo
a exibição de campos específicos, habilitando a funcionalidade de pesquisa e adicionando formatos de exportação.
Atributos:
    list_display (tuple): Campos a serem exibidos na visualização da lista de administração.
    search_fields (tuple): Campos a serem incluídos na funcionalidade de pesquisa.
    resource_class (class): Classe de recurso para exportação de dados.
Métodos:
    get_export_formats(self):
        Estende os formatos de exportação padrão para incluir PDF e XLSX.
"""
@admin.register(Company)
class CompanyAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name', 'address', 'phone')
    resource_class = CompanyResource

    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(PDF)
        formats.append(XLSX)
        return formats


"""
Configuração do Admin para o modelo Employee.
Esta classe personaliza a interface de administração do Django para o modelo Employee,
incluindo opções de exibição, campos de pesquisa, filtros e formatos de exportação.
Atributos:
    list_display (tuple): Campos a serem exibidos na visualização da lista de administração.
    search_fields (tuple): Campos a serem incluídos na funcionalidade de pesquisa.
    list_filter (tuple): Campos a serem incluídos na barra lateral de filtros.
    resource_class (class): Classe de recurso para manipulação de importação/exportação de dados.
Métodos:
    get_export_formats(self):
        Estende os formatos de exportação padrão para incluir PDF e XLSX.
"""
@admin.register(Employee)
class EmployeeAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'standard_check_in', 'standard_check_out', 'auth_code')
    search_fields = ('name', 'email', 'auth_code')
    list_filter = ('company',)
    resource_class = EmployeeResource

    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(PDF)
        formats.append(XLSX)
        return formats

"""
Configuração do Admin para o modelo TimeRecord.
Esta classe personaliza a interface de administração do Django para o modelo TimeRecord,
incluindo opções de exibição, campos de pesquisa, filtros e formatos de exportação.
Atributos:
    list_display (tuple): Campos a serem exibidos na visualização da lista de administração.
    search_fields (tuple): Campos a serem incluídos na funcionalidade de pesquisa.
    list_filter (tuple): Campos a serem incluídos na barra lateral de filtros.
    resource_class (class): Classe de recurso para manipulação de importação/exportação de dados.
Métodos:
    get_export_formats(self):
        Estende os formatos de exportação padrão para incluir PDF e XLSX.
    worked_hours(self, obj):
        Calcula e retorna as horas trabalhadas arredondadas para 2 casas decimais.
        Descrição curta: 'Horas Trabalhadas'.
    lateness(self, obj):
        Calcula e retorna o atraso arredondado para 2 casas decimais.
        Descrição curta: 'Atraso'.
    overtime(self, obj):
        Calcula e retorna as horas extras arredondadas para 2 casas decimais.
        Descrição curta: 'Horas Extras'.
"""
@admin.register(TimeRecord)
class TimeRecordAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'break_time', 'check_out', 'worked_hours','lateness','overtime')
    search_fields = ('employee__name', 'employee__auth_code', 'date')
    list_filter = ('date', 'employee__company')
    resource_class = TimeRecordResource

    def get_export_formats(self):
        formats = super().get_export_formats()
        formats.append(PDF)
        formats.append(XLSX)
        return formats

    def worked_hours(self, obj):
        return round(obj.calculate_worked_hours(),2)
    worked_hours.short_description = 'Horas Trabalhadas'

    def lateness(self, obj):
        return round(obj.calculate_lateness(),2)
    lateness.short_description = 'Atraso'

    def overtime(self, obj):
        return round(obj.calculate_overtime(),2)
    overtime.short_description = 'Horas Extras'
