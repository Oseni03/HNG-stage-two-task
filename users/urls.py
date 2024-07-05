from django.urls import path, include


app_name = "users"

auth_urlpatterns = []

users_urlpatterns = []

urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    path("users/", users_urlpatterns),
]