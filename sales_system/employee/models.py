from django.db import models


class Telephone(models.Model):
    country_code = models.CharField(max_length=25)
    region_code = models.CharField(max_length=25)
    number = models.IntegerField()

    def __str__(self):
        num = str(self. number)
        tel = self.country_code + '-' + self.region_code + '-' + num
        return tel

    class Meta:
        unique_together = [['country_code', 'region_code', 'number']]


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, null=True)
    surname = models.CharField(max_length=75)
    second_surname = models.CharField(max_length=75)
    number = models.IntegerField()
    birthdate = models.DateField(null=True)
    date_of_admission = models.DateField()
    email = models.EmailField()
    reference = models.CharField(max_length=200, null=True)
    sector = models.CharField(max_length=100)
    active = models.BooleanField()
    telephone = models.OneToOneField(
        Telephone,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.first_name + ' ' + self.surname
