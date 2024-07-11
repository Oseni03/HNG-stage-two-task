from django.urls import path

from . import views


app_name = "organisations"

urlpatterns = [
    path("", views.OrganisationListCreateViews.as_view(), name="list-create-organisation"),
    path("/<int:pk>", views. OrganisationRetrieveViews.as_view(), name="retrieve-organisation"),
    path("/<int:pk>/users", views.OrganisationUserViews.as_view(), name="add-user"),
]