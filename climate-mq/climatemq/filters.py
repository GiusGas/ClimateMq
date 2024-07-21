from django_filters import filters
from rest_framework_datatables.django_filters.filterset import DatatablesFilterSet
from rest_framework_datatables.django_filters.filters import GlobalFilter

from climatemq.models import Station, Data

class GlobalCharFilter(GlobalFilter, filters.CharFilter):
    pass

class GlobalDateTimeRangeFilter(GlobalFilter, filters.DateTimeFromToRangeFilter):
    pass

class DataFilter(DatatablesFilterSet):
    id = GlobalCharFilter(lookup_expr='icontains')
    value = GlobalCharFilter(lookup_expr='icontains')
    unit_symbol = GlobalCharFilter(field_name='variable__unit__symbol', lookup_expr='icontains')
    variable_name = GlobalCharFilter(field_name='variable__name', lookup_expr='icontains')

    class Meta:
        model = Data
        fields = '__all__'

class StationFilter(DatatablesFilterSet):
    id = GlobalCharFilter(lookup_expr='icontains')
    name = GlobalCharFilter(lookup_expr='icontains')

    class Meta:
        model = Station
        fields = ['id','name']
