# jwt_auth_app/serializers.py
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Add password field to the serializer
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'name', 'email', 'photo', 'password']
        extra_kwargs = {'password': {'write_only': True}}

def create(self, validated_data):
        # Extract password and remove it from the validated data
        password = validated_data.pop('password', None)

        # Create the user object without saving it yet
        user = CustomUser(**validated_data)

        # Set the user's password using set_password to ensure hashing
        user.set_password(password)

        # Save the user to the database
        user.save()
        return user


# # jwt_auth_app/serializers.py
# from rest_framework import serializers
# from .models import CustomUser

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'username', 'name', 'email', 'phone_number', 'photo')
