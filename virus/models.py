from django.db import models
import datetime

# Employee Model
# Logs each employee to login to the app
class Employee(models.Model):
	full_name = models.CharField(max_length=50)
	username = models.CharField(max_length=20)
	phone_num = models.CharField(max_length=40)
	department = models.CharField(max_length=30)
	passcode = models.CharField(max_length=4)

# Breach Model
# Logs breaches between 2 employee models
class Breach(models.Model):
	emp1 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='%(class)s_emp1')
	emp2 = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='%(class)s_emp2')
	date = models.DateField("Date", default=datetime.date.today)

# TestResult Model
# Logs test results, linked to employee
class TestResult(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	result = models.CharField(max_length=16)
	date = models.DateField("Date", default=datetime.date.today)