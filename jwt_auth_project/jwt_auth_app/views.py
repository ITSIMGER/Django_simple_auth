
# jwt_auth_app/views.py
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer
from datetime import timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Extract password from request data
        password = request.data.get('password')

        # Use serializer to validate and save the user data (including password hashing)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Set the user's password using set_password to ensure hashing
        user.set_password(password)
        user.save()

        return Response({'message': 'User registered successfully'})

class UserLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')  # Assuming username is phone number
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token})
            else:
                return Response({'error': 'Invalid credentials'}, status=400)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class UserLogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logout successful'})

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access_token': access_token})
        except:
            return Response({'error': 'Invalid refresh token'}, status=400)
        


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Set the access token's expiration time to 5 minutes
        token.set_exp(lifetime=timedelta(minutes=5))

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        try:
            refresh = RefreshToken(refresh_token)
            # Set the new access token's expiration time to 5 minutes
            new_access_token = str(refresh.access_token)
            return Response({'access_token': new_access_token})
        except:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        
        


