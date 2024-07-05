from django.urls import path, include

from . import views


app_name = "users"

auth_urlpatterns = [
    path("register", views.CreateUserView.as_view(), name="register"),
    path("login", views.CookieTokenObtainPairView.as_view(), name="login"),
]

users_urlpatterns = [
    path("<int:pk>", views.RetrieveProfile.as_view(), name="profile")
]

urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    path("api/users/", include(users_urlpatterns)),
]