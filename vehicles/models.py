from django.db import models
from accounts.models import CustomUser
from decimal import Decimal
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

plate_validator = RegexValidator(
    regex=r'^\d{2}\s[A-Z]\s\d{3}\s[A-Z]{2}$',
    message="Plate format bo'lishi kerak: '12 A 345 BC'."
)

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("make", "name")

    def __str__(self):
        return f"{self.make.name} {self.name}"

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ("inactive", "Faol emas"),
        ("available", "Mavjud"),
        ("rented", "Ijaraga berilgan"),
        ("maintenance", "Ta'mirda"),
    ]


    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="vehicles")
    make = models.ForeignKey(CarMake, on_delete=models.SET_NULL, null=True, blank=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    plate_number = models.CharField(max_length=20, unique=True, validators=[plate_validator])
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    hourly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        display_name = self.name or f"{self.make} {self.model}" if self.make and self.model else "Unknown Vehicle"
        return f"{display_name} ({self.plate_number})"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Normalize plate number
        if self.plate_number:
            self.plate_number = ' '.join(self.plate_number.strip().upper().split())
        
        # Validate plate format
        if self.plate_number and not re.match(r'^\d{2}\s[A-Z]\s\d{3}\s[A-Z]{2}$', self.plate_number):
            raise ValidationError("Plate format bo'lishi kerak: '12 A 345 BC'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
