from django.urls import path

from . import views


app_name = "organisations"

urlpatterns = [
    path("", views.OrganisationListCreateViews.as_view(), name="list-organisation"),
    path("<int:pk>", views.OrganisationRetrieveViews.as_view(), name="retrieve-organisation"),
]