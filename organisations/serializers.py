from rest_framework import serializers

from .models import Organisation


class OrganisationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organisation
        fields = ("id", "name", "description")