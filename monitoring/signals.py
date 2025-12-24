import logging
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event, Alert

logger = logging.getLogger("monitoring")


@receiver(post_save, sender=Event)
def create_alert_on_severe_event(sender, instance: Event, created: bool, **kwargs):
    if not created:
        return

    if instance.severity not in (Event.Severity.HIGH, Event.Severity.CRITICAL):
        return

    def _create():
        alert, made = Alert.objects.get_or_create(event=instance)
        if made:
            logger.warning(
                "Alert generated",
                extra={"event_id": instance.id, "severity": instance.severity},
            )

    transaction.on_commit(_create)
