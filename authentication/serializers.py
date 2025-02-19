from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CustomerProfile, NutritionistProfile


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']  # noqa: E501
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'This email is already in use.'})

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError(
                {'username': 'This username is already in use.'}
            )

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class NutritionistProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = NutritionistProfile
        fields = ['user', 'registration_number', 'phone']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            nutritionist_profile = NutritionistProfile.objects.create(
                user=user, **validated_data
            )

            return nutritionist_profile


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomerProfile
        fields = [
            'user',
            'phone',
            'age',
            'gender',
            'height',
            'weight',
            'nutritional_goal',
            'diet_plan',
            'allergies',
            'last_appointment'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()
            customer_profile = CustomerProfile.objects.create(
                user=user, **validated_data
            )
            return customer_profile
