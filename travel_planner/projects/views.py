from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import TravelProject, ProjectPlace
from .serializers import TravelProjectSerializer, ProjectPlaceSerializer


class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all()
    serializer_class = TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()

        if project.places.filter(visited=True).exists():
            raise ValidationError(
                "Cannot delete project with visited places."
            )

        return super().destroy(request, *args, **kwargs)


class ProjectPlaceViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectPlaceSerializer

    def get_queryset(self):
        return ProjectPlace.objects.filter(
            project_id=self.kwargs["project_pk"]
        )

    def perform_create(self, serializer):
        project = TravelProject.objects.get(
            id=self.kwargs["project_pk"]
        )

        serializer.save(project=project)

    def perform_update(self, serializer):
        place = serializer.save()

        if place.visited:
            project = place.project
            if not project.places.filter(visited=False).exists():
                project.completed = True
                project.save()
