from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Employee, TimeRecord
from .serializers import CompanySerializer, EmployeeSerializer, TimeRecordSerializer
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta

class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Company.

    Métodos herdados de ModelViewSet:
        list: Lista todas as empresas.
        create: Cria uma nova empresa.
        retrieve: Recupera uma empresa específica.
        update: Atualiza uma empresa existente.
        partial_update: Atualiza parcialmente uma empresa existente.
        destroy: Exclui uma empresa.

    Atributos:
        queryset (QuerySet): Conjunto de dados contendo todas as empresas.
        serializer_class (Serializer): Classe de serializer para o modelo Company.
        filter_backends (list): Lista de filtros aplicados à view.
        filterset_fields (list): Campos disponíveis para filtragem.
        search_fields (list): Campos disponíveis para busca.
        ordering_fields (list): Campos disponíveis para ordenação.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address']
    ordering_fields = ['name']

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo Employee.

    Métodos herdados de ModelViewSet:
        list: Lista todos os funcionários.
        create: Cria um novo funcionário.
        retrieve: Recupera um funcionário específico.
        update: Atualiza um funcionário existente.
        partial_update: Atualiza parcialmente um funcionário existente.
        destroy: Exclui um funcionário.

    Atributos:
        queryset (QuerySet): Conjunto de dados contendo todos os funcionários.
        serializer_class (Serializer): Classe de serializer para o modelo Employee.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class TimeRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações CRUD no modelo TimeRecord.

    Métodos herdados de ModelViewSet:
        list: Lista todos os registros de ponto.
        create: Cria um novo registro de ponto.
        retrieve: Recupera um registro de ponto específico.
        update: Atualiza um registro de ponto existente.
        partial_update: Atualiza parcialmente um registro de ponto existente.
        destroy: Exclui um registro de ponto.

    Atributos:
        queryset (QuerySet): Conjunto de dados contendo todos os registros de ponto.
        serializer_class (Serializer): Classe de serializer para o modelo TimeRecord.
        filter_backends (list): Lista de filtros aplicados à view.
        filterset_fields (list): Campos disponíveis para filtragem.
        search_fields (list): Campos disponíveis para busca.
        ordering_fields (list): Campos disponíveis para ordenação.
    """
    queryset = TimeRecord.objects.all()
    serializer_class = TimeRecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'date']
    search_fields = ['employee__name']
    ordering_fields = ['date']

def home(request):
    """
    View para renderizar a página inicial e lidar com as ações de ponto dos funcionários.

    Parâmetros:
        request (HttpRequest): Objeto de solicitação HTTP.

    Retorna:
        HttpResponse: Resposta HTTP com a página inicial renderizada.
    """
    message = None
    message_type = "success"  # Tipo de mensagem padrão é sucesso

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
            if action == "check_in" and not time_record.check_in:
                time_record.check_in = now.time()
                message = f"Ação {action} concluída para {employee.name}"
            elif action == "start_break" and time_record.check_in and not time_record.break_time:
                time_record.break_time = timedelta(minutes=0)  # Inicializa a pausa
                message = f"Ação {action} concluída para {employee.name}"
            elif action == "end_break" and time_record.break_time == timedelta(minutes=0):
                time_record.break_time = now - datetime.combine(now.date(), time_record.check_in)
                message = f"Ação {action} concluída para {employee.name}"
            elif action == "check_out" and not time_record.check_out:
                time_record.check_out = now.time()
                message = f"Ação {action} concluída para {employee.name}"
            else:
                message = "Ação inválida ou duplicada"
                message_type = "danger"

            time_record.save()
        
        return render(request, "home.html", {"message": message, "message_type": message_type})

    return render(request, "home.html")
