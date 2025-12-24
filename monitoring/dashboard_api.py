import secrets
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.pagination import PageNumberPagination

from .models import Event, Alert
from .serializers import EventSerializer, AlertSerializer


class IsAdminRole(BasePermission):
    """
    Admin-only permission:
    Uses your custom User.is_admin_role property.
    """

    message = "Admin access required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and getattr(user, "is_admin_role", False)
        )


class DashboardAlertPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class DashboardAlertListView(APIView):
    """
    Authenticated users (Admin + Analyst):
    List alerts with filters:
      /api/dashboard/alerts/?severity=CRITICAL&status=OPEN&page=1&page_size=10
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        severity = (request.query_params.get("severity") or "").strip().upper()
        alert_status = (request.query_params.get("status") or "").strip().upper()

        qs = Alert.objects.select_related("event").all().order_by("-created_at")

        if severity:
            qs = qs.filter(event__severity=severity)

        if alert_status:
            qs = qs.filter(status=alert_status)

        paginator = DashboardAlertPagination()
        page = paginator.paginate_queryset(qs, request)

        # Build a lightweight response with event details (nice for dashboard)
        results = []
        for a in page:
            results.append(
                {
                    "id": a.id,
                    "status": a.status,
                    "created_at": a.created_at,
                    "event": {
                        "id": a.event_id,
                        "source_name": a.event.source_name,
                        "event_type": a.event.event_type,
                        "severity": a.event.severity,
                        "description": a.event.description,
                        "timestamp": a.event.timestamp,
                    },
                }
            )

        return paginator.get_paginated_response(results)


class DashboardUpdateAlertStatusView(APIView):
    """
    Admin-only:
      PATCH/POST /api/dashboard/alerts/<id>/status/
      body: {"status":"ACKNOWLEDGED"} or {"status":"RESOLVED"}
    """

    permission_classes = [IsAuthenticated, IsAdminRole]

    def patch(self, request, pk: int):
        return self._update(request, pk)

    def post(self, request, pk: int):
        return self._update(request, pk)

    def _update(self, request, pk: int):
        new_status = (request.data.get("status") or "").strip().upper()
        if not new_status:
            return Response(
                {"detail": "status is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Validate against model choices
        valid_statuses = {
            choice[0] for choice in Alert._meta.get_field("status").choices
        }
        if new_status not in valid_statuses:
            return Response(
                {"detail": f"Invalid status. Allowed: {sorted(list(valid_statuses))}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        alert = Alert.objects.select_related("event").filter(pk=pk).first()
        if not alert:
            return Response(
                {"detail": "Alert not found"}, status=status.HTTP_404_NOT_FOUND
            )

        alert.status = new_status
        alert.save(update_fields=["status"])

        # Return your normal serializer (good for APIs)
        return Response(AlertSerializer(alert).data, status=status.HTTP_200_OK)


class CreateAnalystView(APIView):
    """
    Admin-only endpoint:
    Creates an Analyst user in one click and returns credentials.
    """

    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        User = get_user_model()

        username = (request.data.get("username") or "").strip()
        password = request.data.get("password") or ""

        if not username:
            username = f"analyst_{secrets.token_hex(3)}"  # e.g. analyst_a1b2c3

        if not password:
            password = secrets.token_urlsafe(10)

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Username already exists. Choose a different username."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, password=password)
        user.role = User.Roles.ANALYST
        user.is_staff = False
        user.save()

        return Response(
            {
                "message": "Analyst user created successfully",
                "username": username,
                "password": password,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED,
        )


class TestApiView(APIView):
    """
    Admin-only endpoint:
    Creates a CRITICAL event and returns the created event + alert.
    """

    permission_classes = [IsAuthenticated, IsAdminRole]

    @transaction.atomic
    def post(self, request):
        payload = request.data or {}

        source_name = payload.get("source_name") or "Demo-Source"
        event_type = payload.get("event_type") or "INTRUSION"
        description = (
            payload.get("description")
            or f"Demo CRITICAL event at {timezone.now().isoformat()}"
        )

        event = Event.objects.create(
            source_name=source_name,
            event_type=event_type,
            severity="CRITICAL",
            description=description,
        )

        alert = Alert.objects.filter(event=event).first()
        if not alert:
            alert = Alert.objects.create(event=event, status="OPEN")

        return Response(
            {
                "event": EventSerializer(event).data,
                "alert": AlertSerializer(alert).data,
            },
            status=status.HTTP_201_CREATED,
        )
