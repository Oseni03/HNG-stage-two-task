from rest_framework import serializers

from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    orgId = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = Organisation
        fields = ("orgId", "name", "description")
    

class OrganisationUserSerializer(serializers.Serializer):
    userId = serializers.CharField()