from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import status, permissions
from rest_framework_simplejwt import views as jwt_views, tokens as jwt_tokens

from . import serializers, utils


# Create your views here.
class CreateUserView(CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            return utils.success_response(
                "Registration successful",
                {
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.first_name,
                    "email": user.email,
                    "phone": user.phone,
                },
                status.HTTP_201_CREATED,
            )
        return utils.error_response(
            message="Registration unsuccessful", status_code=status.HTTP_400_BAD_REQUEST
        )


class CookieTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = serializers.CookieTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = jwt_tokens.RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            response = utils.success_response(
                message="Login successful.",
                data={
                    "access": access_token,
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.first_name,
                    "email": user.email,
                    "phone": user.phone,
                },
            )
            utils.set_auth_cookie(
                response,
                {
                    settings.ACCESS_TOKEN_COOKIE: access_token,
                    settings.REFRESH_TOKEN_COOKIE: refresh,
                },
            )
            return response
        
        response = utils.error_response(
            "Authentication failed", status_code=status.HTTP_401_UNAUTHORIZED
        )
        utils.reset_auth_cookie(response)
        return response


class RetrieveProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if pk == request.user.id:
            response = utils.success_response(
                message="<message>",
                data={
                    "user_id": request.user.id,
                    "first_name": request.user.first_name,
                    "last_name": request.user.first_name,
                    "email": request.user.email,
                    "phone": request.user.phone,
                },
            )
            return response
        
        response = utils.error_response(
            "<message>", status_code=status.HTTP_404_NOT_FOUND
        )
        return response
