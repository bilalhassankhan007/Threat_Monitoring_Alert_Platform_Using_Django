import logging
from rest_framework import serializers
from .models import Event, Alert

logger = logging.getLogger("monitoring")


class EventIngestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "source_name",
            "event_type",
            "severity",
            "description",
            "timestamp",
        ]
        read_only_fields = ["id", "timestamp"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "source_name",
            "event_type",
            "severity",
            "description",
            "timestamp",
            "created_by",
        ]
        read_only_fields = fields


class AlertSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    severity = serializers.CharField(source="event.severity", read_only=True)

    class Meta:
        model = Alert
        fields = ["id", "event", "severity", "status", "created_at"]
        read_only_fields = fields


class AlertStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["status"]

    def update(self, instance, validated_data):
        old = instance.status
        instance = super().update(instance, validated_data)
        user = self.context["request"].user
        logger.info(
            "Alert status updated",
            extra={
                "alert_id": instance.id,
                "from": old,
                "to": instance.status,
                "by": user.username,
            },
        )
        return instance
