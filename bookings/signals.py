from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Booking
from vehicles.models import Vehicle

@receiver(post_save, sender=Booking)
def update_vehicle_status_on_booking_change(sender, instance, created, **kwargs):
    """Update vehicle status based on booking status"""
    vehicle = instance.vehicle
    
    if instance.status == 'active':
        vehicle.status = 'rented'
    elif instance.status in ['completed', 'cancelled']:
        # Check if there are other active bookings for this vehicle
        active_bookings = Booking.objects.filter(
            vehicle=vehicle,
            status='active'
        ).exclude(id=instance.id)
        
        if not active_bookings.exists():
            vehicle.status = 'available'
    
    vehicle.save(update_fields=['status'])
