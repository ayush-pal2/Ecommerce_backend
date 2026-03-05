from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from categories.models import User
from product.models import Product
from rest_framework_simplejwt.tokens import RefreshToken
from categories.models import UserRole
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from categories.permissions import IsAdmin

import logging
logger = logging.getLogger(__name__)


@api_view(['POST'])
def register(request):

    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", UserRole.CUSTOMER)

    if not username or not password:
        return Response(
            {"message": "username and password is required"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "user already exists"},
            status=400
        )

    try:
        user = User.objects.create(
            username=username,
            role=role
        )
        user.set_password(password)
        user.save()
    except ValueError:
        return Response(
            {"error": "Invalid role"},
            status=400
        )

    logger.info("user is registered")

    return Response(
        {"message": "User registered Successfully"},
        status=status.HTTP_201_CREATED
    )
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")
    
    if not username or not password:
            return Response(
                {"error": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    user = authenticate(username=username, password=password,role=role)
    
    if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    if not user.is_active:
            return Response(
                {"error": "User account is disabled"},
                status=status.HTTP_403_FORBIDDEN
            )
            
    refresh = RefreshToken.for_user(user)
    
    return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)