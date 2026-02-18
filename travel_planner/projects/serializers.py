from rest_framework import serializers
from .models import TravelProject, ProjectPlace
from .services.artic import validate_place


class ProjectPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectPlace
        fields = [
            "id",
            "external_id",
            "title",
            "notes",
            "visited",
            "created_at",
        ]
        read_only_fields = ["id", "title", "created_at"]

    def validate(self, attrs):
        project = self.context.get("project")

        if project and project.places.count() >= 10:
            raise serializers.ValidationError(
                "Maximum 10 places per project allowed."
            )

        external_id = attrs.get("external_id")

        if project and ProjectPlace.objects.filter(
            project=project,
            external_id=external_id
        ).exists():
            raise serializers.ValidationError(
                "This place already exists in the project."
            )

        title = validate_place(external_id)

        if not title:
            raise serializers.ValidationError(
                "Place not found in Art Institute API."
            )

        attrs["title"] = title
        return attrs

class TravelProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = TravelProject
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "completed",
            "places",
            "created_at",
        ]
        read_only_fields = ["id", "completed", "created_at"]
