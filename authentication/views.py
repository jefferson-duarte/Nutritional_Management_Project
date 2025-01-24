from django.shortcuts import redirect, render
from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (CustomerProfileSerializer,
                          NutritionistProfileSerializer)


def login(request):
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
            return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
