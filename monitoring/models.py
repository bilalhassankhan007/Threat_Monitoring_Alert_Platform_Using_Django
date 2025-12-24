from django.conf import settings
from django.db import models


class Event(models.Model):
    class EventTypes(models.TextChoices):
        INTRUSION = "INTRUSION", "Intrusion"
        MALWARE = "MALWARE", "Malware"
        ANOMALY = "ANOMALY", "Anomaly"

    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    source_name = models.CharField(max_length=120)
    event_type = models.CharField(max_length=20, choices=EventTypes.choices)
    severity = models.CharField(max_length=20, choices=Severity.choices, db_index=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events_created",
    )

    class Meta:
        indexes = [
            models.Index(fields=["severity", "timestamp"]),
            models.Index(fields=["event_type", "timestamp"]),
        ]
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"{self.source_name} {self.event_type} {self.severity}"


class Alert(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Acknowledged"
        RESOLVED = "RESOLVED", "Resolved"

    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="alert")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [models.Index(fields=["status", "created_at"])]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Alert({self.event_id}) {self.status}"
