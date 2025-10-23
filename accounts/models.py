from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        OWNER = "owner", "Mashina egasi"
        RENTER = "renter", "Ijara oluvchi"

    role = models.CharField(max_length=10, choices=Roles.choices)
    phone = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"
