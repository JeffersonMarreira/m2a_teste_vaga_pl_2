from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import CompanyViewSet, EmployeeViewSet, TimeRecordViewSet, home

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'time-records', TimeRecordViewSet)

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]
