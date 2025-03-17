from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CustomerProfile
from ..serializers import (CustomerProfileSerializer,
                           CustomerProfileUpdateSerializer,
                           NutritionistProfileSerializer)


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
                        request, errors[error][0]
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


class UpdateCustomerView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authentication/update_customer.html'

    def get(self, request, customer_id):
        try:
            customer = CustomerProfile.objects.get(id=customer_id)
        except CustomerProfile.DoesNotExist:
            return Response(
                {'error': 'Customer not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.nutritionistprofile != customer.nutritionist:
            return Response(
                {'error': 'You are not authorized to view this customer.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CustomerProfileUpdateSerializer(customer)
        return Response({'serializer': serializer, 'customer': customer})

    def post(self, request, customer_id):
        try:
            customer = CustomerProfile.objects.get(id=customer_id)
        except CustomerProfile.DoesNotExist:
            return Response(
                {'error': 'Customer not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.nutritionistprofile != customer.nutritionist:
            return Response(
                {'error': 'You are not authorized to update this customer.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CustomerProfileUpdateSerializer(
            customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'serializer': serializer, 'customer': customer, 'success': True},  # noqa:E501
                template_name='dashboard/nutritionist_dashboard.html'
            )
        return Response({'serializer': serializer, 'customer': customer})
