from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ANALYST = "ANALYST", "Analyst"

    role = models.CharField(
        max_length=20, choices=Roles.choices, default=Roles.ANALYST, db_index=True
    )

    @property
    def is_admin_role(self) -> bool:
        return bool(self.is_superuser or self.is_staff or self.role == self.Roles.ADMIN)
