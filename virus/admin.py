from django.contrib import admin

# Register your models here.

from . models import Employee, Breach, TestResult

admin.site.register(Employee)
admin.site.register(Breach)
admin.site.register(TestResult)