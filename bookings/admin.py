from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'renter', 'start_at', 'end_at', 'status', 'payment_status', 'total_price', 'created_at')
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
