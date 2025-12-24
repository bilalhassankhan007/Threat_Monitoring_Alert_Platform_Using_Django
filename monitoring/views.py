from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Alert
from .serializers import (
    EventIngestSerializer,
    EventSerializer,
    AlertSerializer,
    AlertStatusUpdateSerializer,
)
from .permissions import EventPermissions, AlertPermissions
from .filters import AlertFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("created_by").all()
    permission_classes = [EventPermissions]

    def get_serializer_class(self):
        return EventIngestSerializer if self.action == "create" else EventSerializer


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alert.objects.select_related("event").all()  # avoids N+1
    serializer_class = AlertSerializer
    permission_classes = [AlertPermissions]
    filterset_class = AlertFilter
    ordering_fields = ["created_at", "status", "event__severity"]

    @action(
        methods=["patch"], detail=True, serializer_class=AlertStatusUpdateSerializer
    )
    def status(self, request, pk=None):
        alert = self.get_object()
        serializer = self.get_serializer(alert, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AlertSerializer(alert).data)
