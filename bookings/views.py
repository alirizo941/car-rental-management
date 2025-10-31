from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from decimal import Decimal
from .models import Booking
from .forms import BookingForm, BookingSearchForm

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_form = BookingSearchForm(self.request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data.get('search')
            status = search_form.cleaned_data.get('status')
            payment_status = search_form.cleaned_data.get('payment_status')
            start_date = search_form.cleaned_data.get('start_date')
            end_date = search_form.cleaned_data.get('end_date')
            
            filters = Q()
            if search:
                filters |= Q(vehicle__make__icontains=search) | Q(vehicle__model__icontains=search) | Q(customer_name__icontains=search) | Q(phone_number__icontains=search) | Q(vehicle__plate_number__icontains=search) | Q(renter__username__icontains=search) | Q(renter__first_name__icontains=search) | Q(renter__last_name__icontains=search)
            if status:
                filters &= Q(status=status)
            if payment_status:
                filters &= Q(payment_status=payment_status)
            if start_date:
                filters &= Q(start_date__gte=start_date)
            if end_date:
                filters &= Q(end_date__lte=end_date)
                
            queryset = queryset.filter(filters)
        return queryset.order_by('-created_at', '-id')

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
        try:
            # Save the booking with default status
            booking = form.save(commit=False)
            booking.status = 'pending'  # Default status
            
            # Set default values if not provided
            if not booking.deposit_amount:
                booking.deposit_amount = Decimal('0.00')
            if not booking.paid_amount:
                booking.paid_amount = Decimal('0.00')
                
            booking.save()
            form.save_m2m()  # In case there are many-to-many fields
            
            # Get vehicle display name safely
            vehicle_name = booking.vehicle.name if hasattr(booking.vehicle, 'name') and booking.vehicle.name else str(booking.vehicle)
            plate_number = booking.vehicle.plate_number if hasattr(booking.vehicle, 'plate_number') else ''
            
            messages.success(
                self.request, 
                f'Yangi ijara #{booking.id} muvaffaqiyatli yaratildi! ' \
                f'Mashina: {vehicle_name} ({plate_number})',
                extra_tags='success'
            )
            return redirect('booking_list')
            
        except Exception as e:
            import traceback
            error_message = f'Xatolik yuz berdi: {str(e)}\n{traceback.format_exc()}'
            messages.error(self.request, error_message, extra_tags='danger')
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('booking_list')

    def form_invalid(self, form):
        # Log form errors for debugging
        for field, errors in form.errors.items():
            field_name = form.fields[field].label if field in form.fields else field
            for error in errors:
                messages.error(
                    self.request, 
                    f'{field_name}: {error}',
                    extra_tags='danger'
                )
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Yangi ijara qo\'shish'
        return context

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
