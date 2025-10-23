from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'owner', 'start_date', 'end_date', 'pricing_type', 'is_active', 'created_at')
    list_filter = ('pricing_type', 'is_active', 'start_date', 'created_at')
    search_fields = ('vehicle__name', 'vehicle__plate_number', 'owner__username', 'owner__first_name', 'owner__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Contract Information', {
            'fields': ('owner', 'vehicle', 'start_date', 'end_date', 'is_active')
        }),
        ('Pricing', {
            'fields': ('pricing_type', 'owner_share_percent', 'company_share_percent', 'fixed_payout_amount')
        }),
        ('Terms', {
            'fields': ('min_rental_days', 'enforce_min_rental_days')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
