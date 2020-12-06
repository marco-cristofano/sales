from django.contrib import admin

from employee.models import (
    Employee,
    Telephone
)
admin.site.register(Employee)
admin.site.register(Telephone)
