from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from .models import Booking, Payment
from .forms import PaymentForm

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'bookings/payment_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        booking_id = self.kwargs.get('booking_id')
        if booking_id:
            booking = get_object_or_404(Booking, id=booking_id)
            initial.update({
                'booking': booking,
                'amount': booking.total_price - booking.paid_amount,
                'created_by': self.request.user
            })
        return initial
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Update booking's payment status
        booking = form.cleaned_data['booking']
        booking.update_payment_status()
        booking.save()
        
        messages.success(self.request, _("Payment added successfully!"))
        return response
    
    def get_success_url(self):
        return reverse_lazy('bookings:detail', kwargs={'pk': self.object.booking.id})

class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'bookings/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        booking_id = self.kwargs.get('booking_id')
        if booking_id:
            queryset = queryset.filter(booking_id=booking_id)
        return queryset.select_related('booking', 'booking__vehicle', 'created_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.kwargs.get('booking_id')
        if booking_id:
            context['booking'] = get_object_or_404(Booking, id=booking_id)
        return context
