from django.contrib import admin
from .models import Constant

@admin.register(Constant)
class ConstantAdmin(admin.ModelAdmin):
    list_display = ('min_owner_rental_days', 'min_renter_rental_hours', 'late_fee_percent', 'updated_at')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Rental Settings', {
            'fields': ('min_owner_rental_days', 'min_renter_rental_hours')
        }),
        ('Financial Settings', {
            'fields': ('late_fee_percent', 'default_owner_share_percent', 'default_company_share_percent')
        }),
        ('System Info', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not Constant.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
