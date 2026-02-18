from rest_framework_nested import routers
from .views import TravelProjectViewSet, ProjectPlaceViewSet

router = routers.DefaultRouter()
router.register(r'projects', TravelProjectViewSet)

projects_router = routers.NestedDefaultRouter(
    router, r'projects', lookup='project'
)
projects_router.register(
    r'places',
    ProjectPlaceViewSet,
    basename='project-places'
)

urlpatterns = router.urls + projects_router.urls
