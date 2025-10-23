"""
Utility functions for Car Rental Management System
"""
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from .models import Vehicle, Booking, Contract, Constant


def get_available_vehicles(start_date, end_date, exclude_booking_id=None):
    """
    Get vehicles that are available for booking in the given date range
    """
    # Get vehicles with conflicting bookings
    conflicting_bookings = Booking.objects.filter(
        status__in=['pending', 'active'],
        start_at__lt=end_date,
        end_at__gt=start_date
    )
    
    if exclude_booking_id:
        conflicting_bookings = conflicting_bookings.exclude(id=exclude_booking_id)
    
    conflicting_vehicle_ids = conflicting_bookings.values_list('vehicle_id', flat=True)
    
    # Return available vehicles
    return Vehicle.objects.filter(
        status='available',
        daily_price__gt=0
    ).exclude(
        id__in=conflicting_vehicle_ids
    )


def calculate_booking_price(vehicle, start_at, end_at):
    """
    Calculate the total price for a booking based on vehicle pricing and duration
    """
    duration_hours = (end_at - start_at).total_seconds() / 3600
    duration_days = duration_hours / 24
    
    # If less than 24 hours and hourly price is set, use hourly pricing
    if duration_hours < 24 and vehicle.hourly_price:
        return vehicle.hourly_price * Decimal(str(duration_hours))
    else:
        # Use daily pricing
        return vehicle.daily_price * Decimal(str(duration_days))


def calculate_earnings(booking):
    """
    Calculate owner and company earnings for a booking based on active contract
    """
    # Find active contract for this vehicle
    try:
        contract = Contract.objects.filter(
            vehicle=booking.vehicle,
            is_active=True,
            start_date__lte=booking.start_at.date()
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=booking.end_at.date())
        ).first()
        
        if not contract:
            # No active contract, all earnings go to company
            return Decimal("0.00"), booking.total_price
        
        if contract.pricing_type == "share":
            # Calculate based on percentages
            owner_earned = (booking.total_price * contract.owner_share_percent) / Decimal("100.00")
            company_earned = (booking.total_price * contract.company_share_percent) / Decimal("100.00")
        else:
            # Fixed payout - owner gets fixed amount, rest goes to company
            owner_earned = contract.fixed_payout_amount or Decimal("0.00")
            company_earned = booking.total_price - owner_earned
            
        return owner_earned, company_earned
        
    except Exception:
        # Fallback: all earnings to company
        return Decimal("0.00"), booking.total_price


def get_system_constants():
    """
    Get system constants, create default if not exists
    """
    constants, created = Constant.objects.get_or_create(
        defaults={
            'min_owner_rental_days': 30,
            'min_renter_rental_hours': 1,
            'late_fee_percent': Decimal("10.00"),
            'default_owner_share_percent': Decimal("80.00"),
            'default_company_share_percent': Decimal("20.00"),
        }
    )
    return constants


def validate_booking_duration(start_at, end_at, user_role=None):
    """
    Validate booking duration based on system constants
    """
    constants = get_system_constants()
    duration_hours = (end_at - start_at).total_seconds() / 3600
    
    if user_role == 'renter':
        min_hours = constants.min_renter_rental_hours
        if duration_hours < min_hours:
            return False, f"Minimal ijara muddati {min_hours} soat"
    
    return True, None


def get_vehicle_earnings_summary(vehicle, start_date=None, end_date=None):
    """
    Get earnings summary for a vehicle in a date range
    """
    bookings = vehicle.bookings.filter(status='completed')
    
    if start_date:
        bookings = bookings.filter(start_at__date__gte=start_date)
    if end_date:
        bookings = bookings.filter(end_at__date__lte=end_date)
    
    total_earnings = sum(booking.total_price for booking in bookings)
    owner_earnings = sum(booking.owner_earned for booking in bookings)
    company_earnings = sum(booking.company_earned for booking in bookings)
    
    return {
        'total_earnings': total_earnings,
        'owner_earnings': owner_earnings,
        'company_earnings': company_earnings,
        'booking_count': bookings.count()
    }


def get_owner_earnings_summary(owner, start_date=None, end_date=None):
    """
    Get earnings summary for an owner in a date range
    """
    bookings = Booking.objects.filter(
        vehicle__owner=owner,
        status='completed'
    )
    
    if start_date:
        bookings = bookings.filter(start_at__date__gte=start_date)
    if end_date:
        bookings = bookings.filter(end_at__date__lte=end_date)
    
    total_earnings = sum(booking.owner_earned for booking in bookings)
    total_bookings = bookings.count()
    
    return {
        'total_earnings': total_earnings,
        'booking_count': total_bookings,
        'vehicles_count': owner.vehicles.count()
    }


def get_company_earnings_summary(start_date=None, end_date=None):
    """
    Get company earnings summary in a date range
    """
    bookings = Booking.objects.filter(status='completed')
    
    if start_date:
        bookings = bookings.filter(start_at__date__gte=start_date)
    if end_date:
        bookings = bookings.filter(end_at__date__lte=end_date)
    
    total_earnings = sum(booking.company_earned for booking in bookings)
    total_bookings = bookings.count()
    total_vehicles = Vehicle.objects.count()
    total_contracts = Contract.objects.filter(is_active=True).count()
    
    return {
        'total_earnings': total_earnings,
        'booking_count': total_bookings,
        'vehicles_count': total_vehicles,
        'contracts_count': total_contracts
    }


def send_booking_notification(booking, notification_type):
    """
    Send notification for booking events (placeholder for future implementation)
    """
    # This can be extended to send emails, SMS, or push notifications
    pass


def check_vehicle_availability(vehicle, start_at, end_at, exclude_booking_id=None):
    """
    Check if a vehicle is available for booking in the given time range
    """
    if vehicle.status != 'available':
        return False, "Mashina mavjud emas"
    
    if vehicle.daily_price <= 0:
        return False, "Mashina narxi belgilanmagan"
    
    # Check for conflicting bookings
    conflicting_bookings = Booking.objects.filter(
        vehicle=vehicle,
        status__in=['pending', 'active'],
        start_at__lt=end_at,
        end_at__gt=start_at
    )
    
    if exclude_booking_id:
        conflicting_bookings = conflicting_bookings.exclude(id=exclude_booking_id)
    
    if conflicting_bookings.exists():
        return False, "Bu vaqtda mashina band"
    
    return True, "Mashina mavjud"


def format_currency(amount):
    """
    Format currency amount for display
    """
    return f"{amount:,.2f} so'm"


def get_status_color(status):
    """
    Get color class for status display
    """
    status_colors = {
        'available': 'green',
        'rented': 'red',
        'maintenance': 'yellow',
        'inactive': 'gray',
        'pending': 'yellow',
        'active': 'green',
        'completed': 'blue',
        'cancelled': 'red',
        'unpaid': 'red',
        'partial': 'yellow',
        'paid': 'green',
    }
    return status_colors.get(status, 'gray')
