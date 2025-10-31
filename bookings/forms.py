from django import forms
from .models import Booking
from accounts.models import CustomUser
from vehicles.models import Vehicle
from datetime import datetime, timedelta
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['renter', 'vehicle', 'start_at', 'end_at', 'deposit_amount', 'paid_amount', 'total_price']
        widgets = {
            'renter': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'start_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'deposit_amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'placeholder': 'Depozit miqdori',
                'value': '0.00'
            }),
            'paid_amount': forms.HiddenInput(attrs={'value': '0.00'}),
            'total_price': forms.HiddenInput(attrs={'value': '0.00'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set required fields
        self.fields['renter'].required = True
        self.fields['vehicle'].required = True
        self.fields['start_at'].required = True
        self.fields['end_at'].required = True
        
        # Filter to only show renters and available vehicles
        self.fields['renter'].queryset = CustomUser.objects.filter(role='renter')
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status='available')
        
        # Add empty options
        self.fields['renter'].empty_label = "Ijara oluvchini tanlang"
        self.fields['vehicle'].empty_label = "Mashina tanlang"
        
        # Set default start time to now
        if not self.instance.pk:
            now = datetime.now()
            self.fields['start_at'].initial = now.strftime('%Y-%m-%dT%H:%M')
            self.fields['end_at'].initial = (now + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
            
        # Set default values for optional fields
        if 'deposit_amount' in self.fields:
            self.fields['deposit_amount'].initial = Decimal('0.00')
        if 'paid_amount' in self.fields:
            self.fields['paid_amount'].initial = Decimal('0.00')
        if 'total_price' in self.fields:
            self.fields['total_price'].initial = Decimal('0.00')

    def clean(self):
        cleaned_data = super().clean()
        start_at = cleaned_data.get('start_at')
        end_at = cleaned_data.get('end_at')
        vehicle = cleaned_data.get('vehicle')

        if start_at and end_at:
            if end_at <= start_at:
                raise forms.ValidationError("Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak.")
            
            # Check if vehicle is available during the requested time
            if vehicle:
                conflicting_bookings = Booking.objects.filter(
                    vehicle=vehicle,
                    status__in=['pending', 'active'],
                    start_at__lt=end_at,
                    end_at__gt=start_at
                )
                # Exclude current instance if editing
                if self.instance.pk:
                    conflicting_bookings = conflicting_bookings.exclude(pk=self.instance.pk)
                    
                if conflicting_bookings.exists():
                    raise forms.ValidationError("Bu vaqtda mashina band.")

        return cleaned_data

class BookingSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Booking qidirish...',
            'id': 'search-input'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'Barcha holatlar')] + Booking.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    payment_status = forms.ChoiceField(
        choices=[('', 'Barcha to\'lov holatlari')] + Booking.PAYMENT_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
