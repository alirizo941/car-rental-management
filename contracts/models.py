from django.db import models
from accounts.models import CustomUser
from vehicles.models import Vehicle
from decimal import Decimal

class Contract(models.Model):
    PRICING_TYPE = [
        ("share", "Revenue share (foizga)"),
        ("fixed", "Fixed payout"),
    ]
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="contracts")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="contracts")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    pricing_type = models.CharField(max_length=10, choices=PRICING_TYPE, default="share")

    owner_share_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    company_share_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fixed_payout_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    min_rental_days = models.PositiveIntegerField(null=True, blank=True)
    enforce_min_rental_days = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("owner", "vehicle", "start_date")
        ordering = ['-created_at']

    def __str__(self):
        return f"Contract: {self.owner.username} - {self.vehicle.plate_number}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from constants.models import Constant
        
        # Validate dates
        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")
        
        # Validate pricing type specific fields
        if self.pricing_type == "share":
            if not self.owner_share_percent or not self.company_share_percent:
                # Use default values from constants
                try:
                    constants = Constant.objects.first()
                    if constants:
                        self.owner_share_percent = constants.default_owner_share_percent
                        self.company_share_percent = constants.default_company_share_percent
                except:
                    self.owner_share_percent = Decimal("80.00")
                    self.company_share_percent = Decimal("20.00")
            
            # Validate percentages sum to 100
            if self.owner_share_percent and self.company_share_percent:
                total = self.owner_share_percent + self.company_share_percent
                if total != Decimal("100.00"):
                    raise ValidationError("Owner and company share percentages must sum to 100%.")
        
        elif self.pricing_type == "fixed":
            if not self.fixed_payout_amount:
                raise ValidationError("Fixed payout amount is required for fixed pricing type.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
