from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response

from employee.serializers import (
    BasicEmployeeSerializer,
    EmployeeSerializer,
    TelephoneSerializer
)
from employee.models import (
    Employee,
    Telephone
)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # Configuracion del filtrado simple
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['number']

    @action(detail=True, methods=['get'], url_path='basic')
    def basic_retrieve(self, request, pk=None):
        employee = self.get_object()
        serializer = BasicEmployeeSerializer(employee)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='basic')
    def basic_list(self, request):
        employees = self.get_queryset()
        serializer = BasicEmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class TelephoneViewSet(viewsets.ModelViewSet):
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer

    def destroy(self, request, pk=None):
        telephone = self.get_object()
        # OneToOne no permite preguntar de una forma sencilla si la
        # relacion está establecida
        if not hasattr(telephone, 'employee'):
            self.perform_destroy(telephone)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'exist related employee', status=status.HTTP_400_BAD_REQUEST)
