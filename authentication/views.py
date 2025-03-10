from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CustomerAdditionalInfoForm
from .models import CustomerProfile, NutritionistProfile
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
            return redirect('additional_info')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_create')
    return render(request, 'authentication/login.html')


def register_nutritionist(request):
    return render(request, 'authentication/nutritionist_registration.html')


def register_customer(request):
    return render(request, 'authentication/customer_registration.html')


# class RegisterNutritionistView(APIView):
#     permission_classes = [AllowAny]
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request):
#         data = request.data.dict()

#         user_data = {
#             'first_name': data.pop('user[first_name]'),
#             'last_name': data.pop('user[last_name]'),
#             'username': data.pop('user[username]'),
#             'email': data.pop('user[email]'),
#             'password': data.pop('user[password]'),
#             'confirm_password': data.pop('user[confirm_password]'),
#         }
#         data['user'] = user_data

#         serializer = NutritionistProfileSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             messages.success(request, 'Nutritionist registered successfully')
#             return redirect('login_create')
#         else:
#             for field, errors in serializer.errors.items():
#                 for error in errors:
#                     messages.error(
#                         request, f"Erro no campo '{field}': {error}"
#                     )
#             return redirect('register_nutritionist')


class RegisterNutritionistView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        serializer = NutritionistProfileSerializer()
        return render(request, 'authentication/nutritionist_registration.html', {'form': serializer})  # noqa:E501

    def post(self, request):
        data = request.data.dict()

        user_data = {
            'first_name': data.pop('user[first_name]', ''),
            'last_name': data.pop('user[last_name]', ''),
            'username': data.pop('user[username]', ''),
            'email': data.pop('user[email]', ''),
            'password': data.pop('user[password]', ''),
            'confirm_password': data.pop('user[confirm_password]', ''),
        }
        data['user'] = user_data

        serializer = NutritionistProfileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Nutritionist registered successfully')
            return redirect('login_create')
        else:
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(
                        request, f"Erro no campo '{field}': {error}"
                    )
            return render(request, 'authentication/nutritionist_registration.html', {'form': serializer})  # noqa:E501


class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomerProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Customer registered successfully'}, status=status.HTTP_201_CREATED)  # noqa:E501

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def additional_info(request):
    nutritionist_profile = NutritionistProfile.objects.filter(user=request.user)  # noqa:E501

    if nutritionist_profile.exists():
        return redirect('dashboard')

    try:
        customer_profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        return redirect('register_customer')

    if customer_profile.profile_complete:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomerAdditionalInfoForm(
            request.POST,
            request.FILES,
            instance=customer_profile
        )
        if form.is_valid():
            form.save()
            customer_profile.profile_complete = True
            customer_profile.save()
            return redirect('dashboard')
    else:
        form = CustomerAdditionalInfoForm(instance=customer_profile)

    return render(
        request,
        'authentication/additional_info.html',
        {'form': form}
    )
