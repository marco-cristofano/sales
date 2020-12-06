from rest_framework import serializers


class EmployeeValidator:

    @classmethod
    def validate(cls, data):
        return cls.validate_date_of_admission(data)

    @classmethod
    def validate_date_of_admission(cls, data):
        # solo verifico si el campo opcional birthdate está presente
        if (data.get('birthdate') and
                data['date_of_admission'] <= data['birthdate']):
            raise serializers.ValidationError(
                {'error_de_negocio': 'birthdate greater than date_of_admission'})
        return data
