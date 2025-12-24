from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, AlertViewSet
from .dashboard_api import (
    CreateAnalystView,
    TestApiView,
    DashboardAlertListView,
    DashboardUpdateAlertStatusView,
)

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="events")
router.register(r"alerts", AlertViewSet, basename="alerts")

urlpatterns = [
    # /api/events/  /api/alerts/
    path("", include(router.urls)),
    # Dashboard helper APIs
    path(
        "dashboard/create-analyst/",
        CreateAnalystView.as_view(),
        name="dashboard-create-analyst",
    ),
    path("dashboard/test-api/", TestApiView.as_view(), name="dashboard-test-api"),
    # ✅ NEW: list alerts + update status
    path(
        "dashboard/alerts/", DashboardAlertListView.as_view(), name="dashboard-alerts"
    ),
    path(
        "dashboard/alerts/<int:pk>/status/",
        DashboardUpdateAlertStatusView.as_view(),
        name="dashboard-alert-status",
    ),
]
