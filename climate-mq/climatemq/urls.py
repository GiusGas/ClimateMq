from django.urls import path

from climatemq.views import StationsMapView

app_name = "climatemq"

urlpatterns = [
    path(
        "map/", StationsMapView.as_view()
    ),
]