from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import CarMake, CarModel, Vehicle
from .forms import CarMakeForm, CarModelForm, VehicleForm, VehicleSearchForm

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 12

    def get_queryset(self):
        queryset = Vehicle.objects.select_related('owner', 'make', 'model')
        
        # Apply search filters
        search_form = VehicleSearchForm(self.request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data.get('search')
            make = search_form.cleaned_data.get('make')
            status = search_form.cleaned_data.get('status')
            min_price = search_form.cleaned_data.get('min_price')
            max_price = search_form.cleaned_data.get('max_price')
            
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(plate_number__icontains=search) |
                    Q(make__name__icontains=search) |
                    Q(model__name__icontains=search)
                )
            
            if make:
                queryset = queryset.filter(make=make)
            
            if status:
                queryset = queryset.filter(status=status)
            
            if min_price:
                queryset = queryset.filter(daily_price__gte=min_price)
            
            if max_price:
                queryset = queryset.filter(daily_price__lte=max_price)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = VehicleSearchForm(self.request.GET)
        context['makes'] = CarMake.objects.all()
        return context

class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, 'Mashina muvaffaqiyatli qo\'shildi!')
        return super().form_valid(form)

class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, 'Mashina muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Mashina muvaffaqiyatli o\'chirildi!')
        return super().delete(request, *args, **kwargs)

@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    bookings = vehicle.bookings.all()[:10]  # Last 10 bookings
    contracts = vehicle.contracts.all()
    
    context = {
        'vehicle': vehicle,
        'bookings': bookings,
        'contracts': contracts,
    }
    return render(request, 'vehicles/vehicle_detail.html', context)

# CarMake views
class CarMakeListView(ListView):
    model = CarMake
    template_name = 'vehicles/carmake_list.html'
    context_object_name = 'makes'
    paginate_by = 20

class CarMakeCreateView(CreateView):
    model = CarMake
    form_class = CarMakeForm
    template_name = 'vehicles/carmake_form.html'
    success_url = reverse_lazy('carmake_list')

    def form_valid(self, form):
        messages.success(self.request, 'Mashina markasi muvaffaqiyatli qo\'shildi!')
        return super().form_valid(form)

# CarModel views
class CarModelListView(ListView):
    model = CarModel
    template_name = 'vehicles/carmodel_list.html'
    context_object_name = 'models'
    paginate_by = 20

class CarModelCreateView(CreateView):
    model = CarModel
    form_class = CarModelForm
    template_name = 'vehicles/carmodel_form.html'
    success_url = reverse_lazy('carmodel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Mashina modeli muvaffaqiyatli qo\'shildi!')
        return super().form_valid(form)

# AJAX view for getting models by make
@login_required
def get_models_by_make(request):
    """AJAX endpoint to get models filtered by make"""
    make_id = request.GET.get('make_id')
    if make_id:
        models = CarModel.objects.filter(make_id=make_id).values('id', 'name')
        return JsonResponse(list(models), safe=False)
    return JsonResponse([], safe=False)
