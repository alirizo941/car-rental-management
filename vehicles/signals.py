from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Vehicle
from contracts.models import Contract

@receiver(post_save, sender=Vehicle)
def update_vehicle_status_on_price_change(sender, instance, created, **kwargs):
    """Update vehicle status to available when daily_price is set and active contract exists"""
    if not created and instance.daily_price > 0:
        # Check if there's an active contract for this vehicle
        active_contract = Contract.objects.filter(
            vehicle=instance,
            is_active=True
        ).first()
        
        if active_contract and instance.status == 'inactive':
            instance.status = 'available'
            instance.save(update_fields=['status'])

@receiver(post_save, sender=Contract)
def update_vehicle_status_on_contract_creation(sender, instance, created, **kwargs):
    """Update vehicle status to available when active contract is created and price is set"""
    if created and instance.is_active and instance.vehicle.daily_price > 0:
        if instance.vehicle.status == 'inactive':
            instance.vehicle.status = 'available'
            instance.vehicle.save(update_fields=['status'])
