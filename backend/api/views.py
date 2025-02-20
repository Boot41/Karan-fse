from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def register_user(request):
    """ API endpoint to register a new user """
    data = request.data
    if User.objects.filter(username=data.get("username")).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=data["username"],
        email=data.get("email", ""),
        password=make_password(data["password"]),
    )
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
