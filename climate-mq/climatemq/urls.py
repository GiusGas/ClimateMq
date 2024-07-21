from django.urls import path

from climatemq.views import StationsMapView, StationsListView, StationsDashboardView, StationDashboardView

app_name = "climatemq"

urlpatterns = [
    path(
        "map/", StationsMapView.as_view()
    ),
    path("stations_list/", StationsListView.as_view()),
    path("dashboard/", StationsDashboardView.as_view()),
    path("dashboard/<int:station_id>", StationDashboardView.as_view()),
]