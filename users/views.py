from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status, permissions
from rest_framework_simplejwt import views as jwt_views, tokens as jwt_tokens

from organisations.models import Organisation

from . import serializers, utils, models


# Create your views here.
class CreateUserView(CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = jwt_tokens.RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return utils.success_response(
            "Registration successful",
            {
                "access_token": access_token,
                "user": {
                    "user_id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.first_name,
                    "email": user.email,
                    "phone": user.phone,
                },
            },
            status.HTTP_201_CREATED,
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
                    "access_token": access_token,
                    "user": {
                        "user_id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.first_name,
                        "email": user.email,
                        "phone": user.phone,
                    },
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


class UserOrganisationViews(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, **kwargs):
        if pk == request.user.id:
            orgs = Organisation.objects.filter(users=request.user)
            response = utils.success_response(
                message="<message>",
                data={
                    "organisations": [
                        {
                            "org_id": org.id,
                            "name": org.name,
                            "description": org.description,
                        }
                        for org in orgs
                    ]
                },
            )
            return response

        response = utils.error_response(
            "<message>", status_code=status.HTTP_404_NOT_FOUND
        )
        return response
