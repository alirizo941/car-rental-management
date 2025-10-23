from django import forms
from .models import Constant

class ConstantForm(forms.ModelForm):
    class Meta:
        model = Constant
        fields = ['min_owner_rental_days', 'min_renter_rental_hours', 'late_fee_percent', 
                 'default_owner_share_percent', 'default_company_share_percent']
        widgets = {
            'min_owner_rental_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimal owner ijara kunlari'}),
            'min_renter_rental_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimal renter ijara soatlari'}),
            'late_fee_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Kechikish foizi'}),
            'default_owner_share_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Default egasi ulushi (%)'}),
            'default_company_share_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Default kompaniya ulushi (%)'})
        }

    def clean(self):
        cleaned_data = super().clean()
        owner_share = cleaned_data.get('default_owner_share_percent')
        company_share = cleaned_data.get('default_company_share_percent')

        if owner_share and company_share:
            if owner_share + company_share != 100:
                raise forms.ValidationError("Default ulushlar jami 100% bo'lishi kerak.")

        return cleaned_data
