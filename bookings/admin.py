from django.contrib import admin
from .models import Booking
from .payment_models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_type', 'payment_method', 'created_at')
    list_filter = ('payment_type', 'payment_method', 'created_at')
    search_fields = ('booking__id', 'booking__renter__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'renter', 'start_at', 'end_at', 'status', 'payment_status', 'total_price', 'paid_amount')
    list_filter = ('status', 'payment_status', 'start_at', 'created_at')
    search_fields = ('vehicle__name', 'vehicle__plate_number', 'renter__username', 'renter__first_name', 'renter__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'owner_earned', 'company_earned')
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('renter', 'vehicle', 'start_at', 'end_at', 'status')
        }),
        ('Payment', {
            'fields': ('payment_status', 'deposit_amount', 'paid_amount')
        }),
        ('Financial', {
            'fields': ('total_price', 'owner_earned', 'company_earned')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
