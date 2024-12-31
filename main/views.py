from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Employee, TimeRecord
from .serializers import CompanySerializer, EmployeeSerializer, TimeRecordSerializer
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']
    ordering_fields = ['name']

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TimeRecordViewSet(viewsets.ModelViewSet):
    queryset = TimeRecord.objects.all()
    serializer_class = TimeRecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'date']
    search_fields = ['employee__name']
    ordering_fields = ['date']

def home(request):
    message = None
    message_type = "success"  # Default message type is success

    if request.method == "POST":
        auth_code = request.POST.get("auth_code")
        action = request.POST.get("action")
        now = datetime.now()

        try:
            employee = get_object_or_404(Employee, auth_code=auth_code)
        except Employee.DoesNotExist:
            message = "Código de autenticação inválido"
            message_type = "danger"
        except Exception as e:
            message = f"Ocorreu um erro: {str(e)}"
            message_type = "danger"
        else:
            time_record, created = TimeRecord.objects.get_or_create(employee=employee, date=now.date())
            print(action)
            if action == "check_in" and not time_record.check_in:
                print('Check in')
                time_record.check_in = now.time()
                message = f"Ação {action} concluída para {employee.name}"
            elif action == "start_break" and time_record.check_in and not time_record.break_time:
                print('Start break')
                time_record.break_time = timedelta(minutes=0)  # Inicializa a pausa
                message = f"Ação {action} concluída para {employee.name}"
            elif action == "end_break" and time_record.break_time == timedelta(minutes=0):
                print('End break')
                time_record.break_time = now - datetime.combine(now.date(), time_record.check_in)
                message = f"Ação {action} concluída para {employee.name}"
            elif action == "check_out" and not time_record.check_out:
                print('Check out')
                time_record.check_out = now.time()
                message = f"Ação {action} concluída para {employee.name}"
            else:
                message = "Ação inválida ou duplicada"
                message_type = "danger"

            time_record.save()
        
        return render(request, "home.html", {"message": message, "message_type": message_type})

    return render(request, "home.html")
