from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Booking
from .forms import BookingForm, BookingSearchForm

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 20

    def get_queryset(self):
        queryset = Booking.objects.select_related('renter', 'vehicle', 'vehicle__make', 'vehicle__model')
        
        # Filter by user role
        user = self.request.user
        if user.role == 'renter':
            queryset = queryset.filter(renter=user)
        elif user.role == 'owner':
            queryset = queryset.filter(vehicle__owner=user)
        elif user.role == 'admin':
            pass  # Show all bookings
        else:
            queryset = queryset.none()
        
        # Apply search filters
        search_form = BookingSearchForm(self.request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data.get('search')
            status = search_form.cleaned_data.get('status')
            payment_status = search_form.cleaned_data.get('payment_status')
            start_date = search_form.cleaned_data.get('start_date')
            end_date = search_form.cleaned_data.get('end_date')
            
            if search:
                queryset = queryset.filter(
                    Q(vehicle__name__icontains=search) |
                    Q(vehicle__plate_number__icontains=search) |
                    Q(renter__username__icontains=search) |
                    Q(renter__first_name__icontains=search) |
                    Q(renter__last_name__icontains=search)
                )
            
            if status:
                queryset = queryset.filter(status=status)
            
            if payment_status:
                queryset = queryset.filter(payment_status=payment_status)
            
            if start_date:
                queryset = queryset.filter(start_at__date__gte=start_date)
            
            if end_date:
                queryset = queryset.filter(end_at__date__lte=end_date)
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = BookingSearchForm(self.request.GET)
        return context

class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        messages.success(self.request, 'Booking muvaffaqiyatli yaratildi!')
        return super().form_valid(form)

class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        messages.success(self.request, 'Booking muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Booking muvaffaqiyatli o\'chirildi!')
        return super().delete(request, *args, **kwargs)

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    user = request.user
    if user.role == 'renter' and booking.renter != user:
        messages.error(request, 'Bu bookingni ko\'rish huquqingiz yo\'q.')
        return redirect('booking_list')
    elif user.role == 'owner' and booking.vehicle.owner != user:
        messages.error(request, 'Bu bookingni ko\'rish huquqingiz yo\'q.')
        return redirect('booking_list')
    elif user.role not in ['admin', 'owner', 'renter']:
        messages.error(request, 'Bu bookingni ko\'rish huquqingiz yo\'q.')
        return redirect('dashboard')
    
    context = {
        'booking': booking,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    user = request.user
    if user.role not in ['admin', 'owner']:
        messages.error(request, 'Bu amalni bajarish huquqingiz yo\'q.')
        return redirect('booking_list')
    
    if user.role == 'owner' and booking.vehicle.owner != user:
        messages.error(request, 'Bu bookingni boshqarish huquqingiz yo\'q.')
        return redirect('booking_list')
    
    new_status = request.POST.get('status')
    if new_status in ['pending', 'active', 'completed', 'cancelled']:
        booking.status = new_status
        booking.save()
        
        status_names = {
            'pending': 'kutilmoqda',
            'active': 'faol',
            'completed': 'tugallangan',
            'cancelled': 'bekor qilingan'
        }
        
        messages.success(request, f'Booking holati "{status_names[new_status]}" ga o\'zgartirildi!')
    
    return redirect('booking_detail', pk=pk)

@login_required
def update_payment_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    user = request.user
    if user.role not in ['admin', 'owner']:
        messages.error(request, 'Bu amalni bajarish huquqingiz yo\'q.')
        return redirect('booking_list')
    
    if user.role == 'owner' and booking.vehicle.owner != user:
        messages.error(request, 'Bu bookingni boshqarish huquqingiz yo\'q.')
        return redirect('booking_list')
    
    new_status = request.POST.get('payment_status')
    if new_status in ['unpaid', 'partial', 'paid']:
        booking.payment_status = new_status
        booking.save()
        
        status_names = {
            'unpaid': 'to\'lanmagan',
            'partial': 'qisman to\'langan',
            'paid': 'to\'langan'
        }
        
        messages.success(request, f'To\'lov holati "{status_names[new_status]}" ga o\'zgartirildi!')
    
    return redirect('booking_detail', pk=pk)
