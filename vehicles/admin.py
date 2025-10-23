from django.contrib import admin
from .models import CarMake, CarModel, Vehicle

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make')
    list_filter = ('make',)
    search_fields = ('name', 'make__name')
    ordering = ('make__name', 'name')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'plate_number', 'make', 'model', 'owner', 'daily_price', 'status', 'created_at')
    list_filter = ('status', 'make', 'owner__role', 'created_at')
    search_fields = ('name', 'plate_number', 'owner__username', 'owner__first_name', 'owner__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'make', 'model', 'name', 'plate_number', 'year')
        }),
        ('Pricing', {
            'fields': ('daily_price', 'hourly_price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
