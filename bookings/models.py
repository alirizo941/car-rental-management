from django.db import models
from accounts.models import CustomUser
from vehicles.models import Vehicle
from contracts.models import Contract
from decimal import Decimal
import math
from django.core.exceptions import ValidationError

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("partial", "Partial"),
        ("paid", "Paid"),
    ]
    
    renter = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid")
    
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    owner_earned = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    company_earned = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} {self.vehicle.plate_number}"

    def duration_hours(self):
        delta = self.end_at - self.start_at
        return max(0, math.ceil(delta.total_seconds() / 3600))

    def duration_days(self):
        return math.ceil(self.duration_hours() / 24)

    def calculate_total_price(self):
        """Calculate total price based on vehicle pricing and duration"""
        hours = self.duration_hours()
        days = self.duration_days()
        
        # If less than 24 hours and hourly price is set, use hourly pricing
        if hours < 24 and self.vehicle.hourly_price:
            return self.vehicle.hourly_price * hours
        else:
            # Use daily pricing
            return self.vehicle.daily_price * days

    def calculate_earnings(self):
        """Calculate owner and company earnings based on active contract"""
        from contracts.models import Contract
        
        # Find active contract for this vehicle
        try:
            contract = Contract.objects.filter(
                vehicle=self.vehicle,
                is_active=True,
                start_date__lte=self.start_at.date()
            ).filter(
                models.Q(end_date__isnull=True) | models.Q(end_date__gte=self.end_at.date())
            ).first()
            
            if not contract:
                # No active contract, all earnings go to company
                self.owner_earned = Decimal("0.00")
                self.company_earned = self.total_price
                return
            
            if contract.pricing_type == "share":
                # Calculate based on percentages
                self.owner_earned = (self.total_price * contract.owner_share_percent) / Decimal("100.00")
                self.company_earned = (self.total_price * contract.company_share_percent) / Decimal("100.00")
            else:
                # Fixed payout - owner gets fixed amount, rest goes to company
                self.owner_earned = contract.fixed_payout_amount or Decimal("0.00")
                self.company_earned = self.total_price - self.owner_earned
                
        except Exception:
            # Fallback: all earnings to company
            self.owner_earned = Decimal("0.00")
            self.company_earned = self.total_price

    def clean(self):
        from constants.models import Constant
        
        if self.end_at <= self.start_at:
            raise ValidationError("End time must be after start time.")
        
        # Check minimum rental duration
        try:
            constants = Constant.objects.first()
            if constants:
                min_hours = constants.min_renter_rental_hours
                if self.duration_hours() < min_hours:
                    raise ValidationError(f"Minimum rental duration is {min_hours} hours.")
        except:
            pass

    def save(self, *args, **kwargs):
        # Calculate total price and earnings before saving
        self.total_price = self.calculate_total_price()
        self.calculate_earnings()
        
        self.clean()
        super().save(*args, **kwargs)
