from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

import datetime
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser

from virus.models import Employee, Breach, TestResult
from .models import AuthToken, Bluetooth

from .tools import GenerateToken

class LoginAPI(GenericAPIView):
	def post(self, request, *args, **kwargs):
		username = request.data['username']
		passcode = request.data['passcode']

		try:
			employee = Employee.objects.get(username=username)
		except Employee.DoesNotExist:
			employee = None

		if employee:
			if employee.passcode == passcode:

				try:
					token = AuthToken.objects.get(employee=employee)
				except AuthToken.DoesNotExist:
					token = None

				if token:
					authToken = token.token
				else:
					authToken = GenerateToken()
					AuthToken.objects.create( employee=employee, token=authToken )

				content = { 'message': 'Logged in', 'status': '200', 'token': authToken }
				stat = status.HTTP_200_OK
			else:
				content = { 'message': 'Not Authorised', 'status': '401', 'token': ''}
				stat = status.HTTP_401_UNAUTHORIZED
		else:
			content = { 'message': 'Not Found!', 'status': '404', 'token': ''}
			stat = status.HTTP_404_NOT_FOUND

		return Response(content, status=stat)



class LogoutAPI(GenericAPIView):
	def post(self, request, *args, **kwargs):
		request.session['auth'] = False
		content = {'Goodbye': 'Come back soon!'}
		return Response(content, status=status.HTTP_200_OK)



class BreachAPI(GenericAPIView):
	def post(self, request, *args, **kwargs):
		authToken = request.data['token']
		uuid = request.data['uuid']

		try:
			auth = AuthToken.objects.get( token=authToken )
		except AuthToken.DoesNotExist:
			auth = None

		if auth:
			employee = auth.employee
			secondEmp = None
			uuids = Bluetooth.objects.filter( uuid=uuid )

			for blue in uuids:
				secondEmp = blue.employee

			if secondEmp:
				Breach.objects.create( emp1=employee, emp2=secondEmp )
				content = { 'message': 'Created Breach', 'status': '201' }
				stat = status.HTTP_201_CREATED
			else:
				content = { 'message': 'Not Found!', 'status': '404' }
				stat = status.HTTP_404_NOT_FOUND

		else:
			content = { 'message': 'Not Authorised', 'status': '401'}
			stat = status.HTTP_401_UNAUTHORIZED

		return Response(content, status=stat)



class ResultAPI(GenericAPIView):
	def post(self, request, *args, **kwargs):
		authToken = request.data['token']
		result = request.data['result']

		try:
			auth = AuthToken.objects.get( token=authToken )
		except AuthToken.DoesNotExist:
			auth = None

		if auth:
			employee = auth.employee
			TestResult.objects.create( employee=employee, result=result )
			content = { 'message': 'Created Result Entry', 'status': '201' }
			stat = status.HTTP_201_CREATED
		else:
			content = { 'message': 'Not Authorised', 'status': '401'}
			stat = status.HTTP_401_UNAUTHORIZED

		return Response(content, status=stat)



class BluetoothAPI(GenericAPIView):
	def post(self, request, *args, **kwargs):
		authToken = request.data['token']
		uuid = request.data['uuid']

		try:
			auth = AuthToken.objects.get( token=authToken )
		except AuthToken.DoesNotExist:
			auth = None

		if auth:
			employee = auth.employee
			Bluetooth.objects.create( employee=employee, uuid=uuid )
			content = { 'message': 'Created Bluetooth Entry', 'status': '201' }
			stat = status.HTTP_201_CREATED
		else:
			content = { 'message': 'Not Authorised', 'status': '401'}
			stat = status.HTTP_401_UNAUTHORIZED

		return Response(content, status=stat)