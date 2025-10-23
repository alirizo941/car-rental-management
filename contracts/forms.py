from django import forms
from .models import Contract
from accounts.models import CustomUser
from vehicles.models import Vehicle

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['owner', 'vehicle', 'start_date', 'end_date', 'pricing_type', 
                 'owner_share_percent', 'company_share_percent', 'fixed_payout_amount',
                 'min_rental_days', 'enforce_min_rental_days', 'notes']
        widgets = {
            'owner': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md'
            }),
            'vehicle': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'type': 'date'
            }),
            'pricing_type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md'
            }),
            'owner_share_percent': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'step': '0.01',
                'placeholder': 'Egasi ulushi (%)',
                'min': '0',
                'max': '100'
            }),
            'company_share_percent': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'step': '0.01',
                'placeholder': 'Kompaniya ulushi (%)',
                'min': '0',
                'max': '100'
            }),
            'fixed_payout_amount': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'step': '1000',
                'placeholder': 'Belgilangan to\'lov (so\'m)',
                'min': '0'
            }),
            'min_rental_days': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'placeholder': 'Minimal ijara kunlari',
                'min': '1'
            }),
            'enforce_min_rental_days': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md',
                'rows': 3,
                'placeholder': 'Qo\'shimcha ma\'lumotlar'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter to only show owners and their vehicles
        self.fields['owner'].queryset = CustomUser.objects.filter(role='owner')
        self.fields['vehicle'].queryset = Vehicle.objects.filter(owner__role='owner')
        
        # Add empty options
        self.fields['owner'].empty_label = "Egasi tanlang"
        self.fields['vehicle'].empty_label = "Mashina tanlang"

    def clean(self):
        cleaned_data = super().clean()
        pricing_type = cleaned_data.get('pricing_type')
        owner_share = cleaned_data.get('owner_share_percent')
        company_share = cleaned_data.get('company_share_percent')
        fixed_payout = cleaned_data.get('fixed_payout_amount')

        if pricing_type == 'share':
            if not owner_share or not company_share:
                raise forms.ValidationError("Share rejimi uchun egasi va kompaniya ulushlari kiritilishi kerak.")
            if owner_share + company_share != 100:
                raise forms.ValidationError("Ulushlar jami 100% bo'lishi kerak.")
        elif pricing_type == 'fixed':
            if not fixed_payout:
                raise forms.ValidationError("Fixed rejimi uchun belgilangan to'lov miqdori kiritilishi kerak.")

        return cleaned_data
