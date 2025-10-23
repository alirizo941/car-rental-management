from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Constant
from .forms import ConstantForm

@login_required
def constants_list(request):
    # Only admin can access constants
    if request.user.role != 'admin':
        messages.error(request, 'Bu sahifani ko\'rish huquqingiz yo\'q.')
        return redirect('dashboard')
    
    constants = Constant.objects.first()
    if not constants:
        constants = Constant.objects.create()
    
    if request.method == 'POST':
        form = ConstantForm(request.POST, instance=constants)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sozlamalar muvaffaqiyatli yangilandi!')
            return redirect('constants_list')
    else:
        form = ConstantForm(instance=constants)
    
    context = {
        'constants': constants,
        'form': form,
    }
    return render(request, 'constants/constants_list.html', context)
