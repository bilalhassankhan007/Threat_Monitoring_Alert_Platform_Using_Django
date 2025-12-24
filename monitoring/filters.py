import django_filters
from .models import Alert


class AlertFilter(django_filters.FilterSet):
    severity = django_filters.CharFilter(
        field_name="event__severity", lookup_expr="iexact"
    )
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Alert
        fields = ["severity", "status"]
