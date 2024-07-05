from rest_framework import status, permissions, mixins
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView

from users import utils

from . import serializers, models


# Create your views here.
class OrganisationRetrieveViews(RetrieveAPIView):
    serializer_class = serializers.OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Organisation.objects.filter(users=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            organisation = self.get_object()
            data = {
                "org_id": organisation.id,
                "name": organisation.name,
                "description": organisation.description,
            }
            response = utils.success_response("<message>", data)
            return response
        except:
            response = utils.error_response("<message>")
            return response


class OrganisationListCreateViews(ListCreateAPIView):
    serializer_class = serializers.OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.Organisation.objects.filter(users=self.request.user)

    def list(self, request, *args, **kwargs):
        try:
            organisations = self.get_queryset()
            data = [
                {"org_id": org.id, "name": org.name, "description": org.description}
                for org in organisations
            ]
            response = utils.success_response("<message>", data={"organisations": data})
            return response
        except:
            response = utils.error_response("<message>")
            return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            org = serializer.save()
            return utils.success_response(
                "Organisation created successfully",
                {
                    "org_id": org.id,
                    "name": org.name,
                    "description": org.description,
                },
                status.HTTP_201_CREATED,
            )
        return utils.error_response(
            message="Client error", status_code=status.HTTP_400_BAD_REQUEST
        )
