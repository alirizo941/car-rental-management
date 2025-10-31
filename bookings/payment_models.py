from django.db import models
from django.utils import timezone
from .models import Booking

class Payment(models.Model):
    PAYMENT_TYPES = [
        ('deposit', 'Depozit'),
        ('advance', 'Oldindan to\'lov'),
        ('final', 'Yakuniy to\'lov'),
        ('other', 'Boshqa')
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Naqd pul'),
        ('card', 'Plastik karta'),
        ('transfer', 'Bank orqali'),
        ('other', 'Boshqa')
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"To'lov #{self.id} - {self.amount} UZS"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update booking's paid amount
        self.booking.update_payment_status()
        self.booking.save()
