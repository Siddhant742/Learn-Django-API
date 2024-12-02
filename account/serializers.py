from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Password is required.'
    })
    email = serializers.EmailField(required=True, error_messages={
        'required': 'Email is required.'
    })
    username = serializers.CharField(required=True, error_messages={
        'required': 'Username is required.'
    })
    first_name = serializers.CharField(required=True, error_messages={
        'required': 'First name is required.'
    })
    last_name = serializers.CharField(required=True, error_messages={
        'required': 'Last name is required.'
    })

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, error_messages={
        'required': 'Username is required.'
    })
    password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Password is required.'
    })

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
                return user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")