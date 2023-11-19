from django.db import models

from virus.models import Employee

# Create your models here.
class AuthToken(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	token = models.CharField(max_length=16)

class Bluetooth(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	uuid = models.CharField(max_length=64)