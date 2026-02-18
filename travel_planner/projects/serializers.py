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


class TravelProjectCreateSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = TravelProject
        fields = ["id", "name", "description", "start_date", "places"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        places_data = validated_data.pop("places", [])
        project = TravelProject.objects.create(**validated_data)

        for place_data in places_data:
            external_id = place_data["external_id"]
            title = validate_place(external_id)
            if title:
                ProjectPlace.objects.create(
                    project=project,
                    external_id=external_id,
                    title=title
                )
        return project