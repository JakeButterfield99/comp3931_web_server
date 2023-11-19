from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Employee, Breach, TestResult
from api.models import Bluetooth

import datetime

# Create your views here.

# Index page, redirect to home if logged in
def index(request):
	template = "virus/index.html"
	title = "VirusAdmin | Login"

	# Check if user is logged in
	if request.user.is_authenticated:
		return home(request)

	return render(request,
				template,
				{'title': title})


# Home Page, Staff list + New Staff
def home(request):
	if not request.user.is_authenticated:
		return index(request)

	template = "virus/home.html"
	title = "VirusAdmin | Staff List"

	# Process POST request, form submit
	if request.method == "POST":
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		dept = request.POST.get('dept')
		username = request.POST.get('username')
		passcode = request.POST.get('passcode')

		# Insert into database
		Employee.objects.create( full_name=name, username=username, passcode=passcode, phone_num=phone, department=dept )	
 
 	# Get all employees
	employees = Employee.objects.all()

	# Return template, with list of employees
	return render(request,
				template,
				{'title': title, 'employees': employees})


def breach(request):
	if not request.user.is_authenticated:
		return index(request)

	template = "virus/breach.html"
	title = "VirusAdmin | Breach List"

	# POST Request, for submit
	if request.method == "POST":
		emp1ID = request.POST.get('employee1')
		emp2ID = request.POST.get('employee2')

		emp1 = Employee.objects.get(id=emp1ID)
		emp2 = Employee.objects.get(id=emp2ID)

		# Insert into database
		Breach.objects.create( emp1=emp1, emp2=emp2 )	

	# Get Latest breaches and all employees
	breaches = Breach.objects.all().order_by('-date')
	employees = Employee.objects.all()

	# Return template with employee list and breaches
	return render(request,
				template,
				{'title': title, 'breaches': breaches, 'employees': employees})


possibleResults = {'0': 'Negative', '1': 'Positive'}
def report(request):
	if not request.user.is_authenticated:
		return index(request)

	template = "virus/report.html"
	title = "VirusAdmin | Report Case"
	
	# POST request, form submit
	if request.method == "POST":
		empID = request.POST.get('employee')
		resID = request.POST.get('result')

		# Get Employee from ID
		employee = Employee.objects.get(id=empID)
		result = possibleResults[resID]

		# Insert test result into database
		TestResult.objects.create( employee=employee, result=result )


	# Get all results, sort by date
	results = TestResult.objects.all().order_by('-date')
	employees = Employee.objects.all()

	# Return template, results and employees
	return render(request,
				template,
				{'title': title, 'results': results, 'employees': employees})


def search(request):
	if not request.user.is_authenticated:
		return index(request)

	template = "virus/search.html"
	title = "VirusAdmin | Search"

	# POST Request, form submit
	if request.method == "POST":
		name = request.POST.get('name')

		# find the employee with similar name
		employee = Employee.objects.filter(full_name__icontains=name).first()

		# Redirect if employee is found
		if employee:
			return redirect('edit', empID=employee.id)

	return render(request,
				template,
				{'title': title})


def edit(request, empID):
	if not request.user.is_authenticated:
		return index(request)

	template = "virus/edit.html"
	title = "VirusAdmin | Edit"

	# Get employee data, bluetooth and results
	employee = Employee.objects.get(id=empID)
	bluetooth = Bluetooth.objects.filter(employee=employee).last()
	results = TestResult.objects.filter(employee=employee).order_by('-date')
	
	# Get breach data for that employee, sort by date
	breaches = Breach.objects.filter(emp1=employee).order_by('-date')

	# Return template, and employee data
	return render(request,
				template,
				{'title': title,
				 'employee': employee,
				 'bluetooth': bluetooth,
				 'results': results,
				 'breaches': breaches})


def generate(request, empID):
	if not request.user.is_authenticated:
		return index(request)

	template = "virus/generate.html"
	title = "VirusAdmin | Isolation Report"

	# Get Employee data
	employee = Employee.objects.get(id=empID)

	searchDate = datetime.date.today() - datetime.timedelta(days=3)

	# Get breaches data
	breach1 = Breach.objects.filter(emp1=employee, date__gte=searchDate)
	breach2 = Breach.objects.filter(emp2=employee, date__gte=searchDate)

	isoData = {}

	# Process breach data
	for b in breach1:
		name = b.emp2.full_name
		if name in isoData:
			isoData[name].append( b.date )
		else:
			isoData[name] = []
			isoData[name].append( b.date )

	for b in breach2:
		name = b.emp1.full_name
		if name in isoData:
			isoData[name].append( b.date )
		else:
			isoData[name] = []
			isoData[name].append( b.date )

	return render(request,
				template,
				{'title': title,
				 'employee': employee,
				 'iso': isoData })