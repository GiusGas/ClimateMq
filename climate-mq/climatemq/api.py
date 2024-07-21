from rest_framework import routers

from climatemq.viewsets import (
    StationViewSet,
    LastDataViewSet,
    DataViewSet,
    DataChartViewSet,
    StationTableViewSet
)

router = routers.DefaultRouter()
router.register(
    r"stations", StationViewSet
)
router.register(
    r"table_stations", StationTableViewSet, basename='table_stations'
)
router.register(
    r"datas", DataViewSet
)
router.register(
    r"last_datas", LastDataViewSet, basename='last_datas'
)
router.register(
    r"chart", DataChartViewSet, basename='chart'
)

urlpatterns = router.urls