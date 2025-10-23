from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Contract
from .forms import ContractForm

class ContractListView(ListView):
    model = Contract
    template_name = 'contracts/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 20

    def get_queryset(self):
        queryset = Contract.objects.select_related('owner', 'vehicle', 'vehicle__make', 'vehicle__model')
        
        # Filter by user role
        user = self.request.user
        if user.role == 'owner':
            queryset = queryset.filter(owner=user)
        elif user.role == 'admin':
            pass  # Show all contracts
        else:
            queryset = queryset.none()  # Renters can't see contracts
        
        return queryset.order_by('-created_at')

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contract_list')

    def form_valid(self, form):
        messages.success(self.request, 'Shartnoma muvaffaqiyatli yaratildi!')
        return super().form_valid(form)

class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contract_list')

    def form_valid(self, form):
        messages.success(self.request, 'Shartnoma muvaffaqiyatli yangilandi!')
        return super().form_valid(form)

class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'contracts/contract_confirm_delete.html'
    success_url = reverse_lazy('contract_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Shartnoma muvaffaqiyatli o\'chirildi!')
        return super().delete(request, *args, **kwargs)

@login_required
def contract_detail(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    
    # Check permissions
    user = request.user
    if user.role == 'owner' and contract.owner != user:
        messages.error(request, 'Bu shartnomani ko\'rish huquqingiz yo\'q.')
        return redirect('contract_list')
    elif user.role == 'renter':
        messages.error(request, 'Bu shartnomani ko\'rish huquqingiz yo\'q.')
        return redirect('dashboard')
    
    # Get related bookings
    bookings = contract.vehicle.bookings.filter(
        start_at__date__gte=contract.start_date
    )
    if contract.end_date:
        bookings = bookings.filter(start_at__date__lte=contract.end_date)
    
    context = {
        'contract': contract,
        'bookings': bookings[:20],  # Last 20 bookings
    }
    return render(request, 'contracts/contract_detail.html', context)

@login_required
def toggle_contract_status(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    
    # Check permissions
    user = request.user
    if user.role not in ['admin', 'owner']:
        messages.error(request, 'Bu amalni bajarish huquqingiz yo\'q.')
        return redirect('contract_list')
    
    if user.role == 'owner' and contract.owner != user:
        messages.error(request, 'Bu shartnomani boshqarish huquqingiz yo\'q.')
        return redirect('contract_list')
    
    contract.is_active = not contract.is_active
    contract.save()
    
    status = 'faollashtirildi' if contract.is_active else 'deaktivlashtirildi'
    messages.success(request, f'Shartnoma {status}!')
    
    return redirect('contract_detail', pk=pk)
