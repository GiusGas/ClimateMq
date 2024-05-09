from rest_framework import routers

from climatemq.viewsets import (
    StationViewSet,
)

router = routers.DefaultRouter()
router.register(
    r"stations", StationViewSet
)

urlpatterns = router.urls