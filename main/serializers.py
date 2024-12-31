from rest_framework import serializers
from .models import Company, Employee, TimeRecord

""" Serializer para os modelo Company, Employee e TimeRecord. 
Serializa todos os campos dos modelos para representação JSON. """

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class TimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRecord
        fields = '__all__'