from rest_framework import serializers

from employee.models import (
    Employee,
    Telephone
)
from employee.validations import EmployeeValidator


class TelephoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Telephone
        fields = (
            'country_code',
            'region_code',
            'number'
        )


class EmployeeSerializer(serializers.ModelSerializer):
    validator = EmployeeValidator

    def validate(self, data):
        return self.validator.validate(data)

    class Meta:
        model = Employee
        fields = (
            'first_name',
            'second_name',
            'surname',
            'second_surname',
            'number',
            'birthdate',
            'date_of_admission',
            'email',
            'reference',
            'sector',
            'active',
            'telephone'
        )


class BasicEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'first_name',
            'surname',
            'number',
            'email'
        )
