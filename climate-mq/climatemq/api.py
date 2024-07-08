from rest_framework import routers

from climatemq.viewsets import (
    StationViewSet,
    DataViewSet,
    DataTableSet
)

router = routers.DefaultRouter()
router.register(
    r"stations", StationViewSet
)
router.register(
    r"datas", DataTableSet
)

urlpatterns = router.urls