from django import forms
from .models import CarMake, CarModel, Vehicle
from accounts.models import CustomUser

class CarMakeForm(forms.ModelForm):
    class Meta:
        model = CarMake
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina markasi'})
        }

class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = ['make', 'name']
        widgets = {
            'make': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina modeli'})
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['owner', 'make', 'model', 'name', 'plate_number', 'year', 'daily_price', 'hourly_price', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # CSS klasslari
        css_class = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm py-2 px-3 border border-gray-300 rounded-md'
        
        # Filter owners to only show users with owner role
        self.fields['owner'].queryset = CustomUser.objects.filter(role='owner')
        
        # Add empty option for make and model
        self.fields['make'].empty_label = "Markani tanlang"
        self.fields['model'].empty_label = "Modelni tanlang"
        
        # Widget stillarini yangilash
        self.fields['owner'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Egasi'
        })
        self.fields['make'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Markani tanlang'
        })
        self.fields['model'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Modelni tanlang'
        })
        self.fields['name'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Mashina nomi (ixtiyoriy)'
        })
        self.fields['plate_number'].widget.attrs.update({
            'class': css_class,
            'placeholder': '12 A 345 BC'
        })
        self.fields['year'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Yil (masalan: 2020)',
            'min': '1900',
            'max': '2025'
        })
        self.fields['daily_price'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Kunlik narx (so\'m)',
            'step': '1000',
            'min': '0'
        })
        self.fields['hourly_price'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Soatlik narx (so\'m)',
            'step': '100',
            'min': '0'
        })
        self.fields['status'].widget.attrs.update({
            'class': css_class,
            'placeholder': 'Holatni tanlang'
        })

class VehicleSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mashina qidirish...',
            'id': 'search-input'
        })
    )
    make = forms.ModelChoiceField(
        queryset=CarMake.objects.all(),
        required=False,
        empty_label="Barcha markalar",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=[('', 'Barcha holatlar')] + Vehicle.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Min narx'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Max narx'})
    )
