from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (CustomerProfileSerializer,
                          NutritionistProfileSerializer)


def home(request):
    return render(request, 'authentication/home.html')


def login_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_create')
    return render(request, 'authentication/login.html')


def register_nutritionist(request):
    return render(request, 'authentication/nutritionist_registration.html')


def register_customer(request):
    return render(request, 'authentication/customer_registration.html')


class RegisterNutritionistView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data.dict()

        user_data = {
            'first_name': data.pop('user[first_name]'),
            'last_name': data.pop('user[last_name]'),
            'username': data.pop('user[username]'),
            'email': data.pop('user[email]'),
            'password': data.pop('user[password]'),
            'confirm_password': data.pop('user[confirm_password]'),
        }
        data['user'] = user_data

        serializer = NutritionistProfileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Nutritionist registered successfully')
            return redirect('login_create')

        messages.error(request, 'Error registering nutritionist')
        return redirect('register_nutritionist')


class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data.dict()

        user_data = {
            'first_name': data.pop('user[first_name]'),
            'last_name': data.pop('user[last_name]'),
            'username': data.pop('user[username]'),
            'email': data.pop('user[email]'),
            'password': data.pop('user[password]'),
            'confirm_password': data.pop('user[confirm_password]'),
        }
        data['user'] = user_data

        serializer = CustomerProfileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Customer registered successfully')
            return redirect('login_create')

        messages.error(request, 'Error registering customer')
        return redirect('register_customer')
