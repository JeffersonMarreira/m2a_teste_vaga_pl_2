from django.contrib import admin
from .models import Company, Employee, TimeRecord
from import_export.admin import ExportActionMixin
from .resources import CompanyResource, EmployeeResource, TimeRecordResource
from import_export.formats.base_formats import XLSX
from .pdf_format import PDF
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
