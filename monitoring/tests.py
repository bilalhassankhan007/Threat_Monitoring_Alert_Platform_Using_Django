from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import User
from monitoring.models import Event, Alert


class ThreatPlatformTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin1", password="pass1234", role=User.Roles.ADMIN, is_staff=True
        )
        self.analyst = User.objects.create_user(
            username="analyst1", password="pass1234", role=User.Roles.ANALYST
        )

    def token(self, username, password):
        url = reverse("token_obtain_pair")
        res = self.client.post(
            url, {"username": username, "password": password}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        return res.data["access"]

    def test_high_event_creates_alert(self):
        t = self.token("analyst1", "pass1234")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {t}")

        res = self.client.post(
            "/api/events/",
            {
                "source_name": "Camera-01",
                "event_type": "INTRUSION",
                "severity": "HIGH",
                "description": "Unauthorized entry",
            },
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Alert.objects.filter(event_id=res.data["id"]).exists())

    def test_medium_event_no_alert(self):
        t = self.token("analyst1", "pass1234")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {t}")

        res = self.client.post(
            "/api/events/",
            {
                "source_name": "SIEM",
                "event_type": "ANOMALY",
                "severity": "MEDIUM",
                "description": "Suspicious activity",
            },
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertFalse(Alert.objects.filter(event_id=res.data["id"]).exists())

    def test_analyst_cannot_update_alert(self):
        e = Event.objects.create(
            source_name="X",
            event_type="MALWARE",
            severity="HIGH",
            description="Malware",
        )
        a = Alert.objects.get(event=e)

        t = self.token("analyst1", "pass1234")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {t}")

        res = self.client.patch(
            f"/api/alerts/{a.id}/status/", {"status": "RESOLVED"}, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_alert(self):
        e = Event.objects.create(
            source_name="X",
            event_type="MALWARE",
            severity="HIGH",
            description="Malware",
        )
        a = Alert.objects.get(event=e)

        t = self.token("admin1", "pass1234")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {t}")

        res = self.client.patch(
            f"/api/alerts/{a.id}/status/", {"status": "RESOLVED"}, format="json"
        )
        self.assertEqual(res.status_code, 200)
        a.refresh_from_db()
        self.assertEqual(a.status, "RESOLVED")
