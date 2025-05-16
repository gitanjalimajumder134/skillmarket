from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .firebase import auth as firebase_auth
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
import requests
from django.conf import settings


class RegisterUser(APIView):
    @swagger_auto_schema(
        operation_description="Register new user using Firebase Auth and store in Django DB",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password', 'username'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: "User registered successfully", 400: "Validation error"}
    )
    def get(self, request):
        data = 'hello'
        # email = request.data.get('email')
        # password = request.data.get('password')
        # username = request.data.get('username')

        # if not all([email, password, username]):
        #     return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     firebase_user = firebase_auth.create_user(email=email, password=password)
        # except Exception as e:
        #     return Response({'error': f'Firebase Error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # user = User.objects.create_user(username=username, email=email)
        return Response({'message': 'User registered successfully'},data=data, status=status.HTTP_201_CREATED)

# class LoginUser(APIView):
    @swagger_auto_schema(
        operation_description="Login user using Firebase email & password, issue JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: "JWT token issued", 401: "Invalid credentials", 404: "User not found"}
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔐 Firebase password verification via REST API
        firebase_api_key = settings.FIREBASE_API_KEY
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }


        firebase_response = requests.post(url, json=payload)

        if firebase_response.status_code != 200:
            error_msg = firebase_response.json().get("error", {}).get("message", "Authentication failed")
            # Provide user-friendly messages
            if error_msg == "EMAIL_NOT_FOUND":
                return Response({'error': 'No account found with this email.'}, status=status.HTTP_401_UNAUTHORIZED)
            elif error_msg == "INVALID_PASSWORD":
                return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
            elif error_msg == "USER_DISABLED":
                return Response({'error': 'This account has been disabled.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        # ✅ Check local DB user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User authenticated in Firebase but not found in local database.'},
                            status=status.HTTP_404_NOT_FOUND)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)