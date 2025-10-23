from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.http import JsonResponse
from .forms import UserUpdateForm, CustomUserCreationForm
from .models import CustomUser
from vehicles.models import CarMake, CarModel, Vehicle
import json

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')



@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
      
    return render(request, 'accounts/profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Tizimdan chiqdingiz.')
    return redirect('login')

@login_required
def users_list(request):
    """Mijozlar ro'yxati - faqat owner va renter"""
    # Faqat mijozlarni ko'rsatish (admin emas)
    users = CustomUser.objects.filter(
        role__in=['owner', 'renter']
    ).order_by('-date_joined')
    
    context = {
        'users': users,
    }
    return render(request, 'accounts/users_list.html', context)

class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('users_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mashina markalarini context ga qo'shish
        context['car_makes'] = CarMake.objects.all()
        return context
    
    def form_valid(self, form):
        # Form save metodini chaqirish va user, password olish
        user, generated_password = form.save()
        
        # Mashina ma'lumotlarini tekshirish va saqlash
        vehicles_data = self.request.POST.get('vehicles_data')
        if vehicles_data and user.role == 'owner':
            try:
                vehicles_json = json.loads(vehicles_data)
                for vehicle_data in vehicles_json:
                    # Vehicle obyektini yaratish
                    vehicle = Vehicle(
                        owner=user,
                        make_id=vehicle_data.get('make'),
                        model_id=vehicle_data.get('model'),
                        name=vehicle_data.get('name', ''),
                        plate_number=vehicle_data.get('plate_number'),
                        year=vehicle_data.get('year'),
                        daily_price=vehicle_data.get('daily_price'),
                        hourly_price=vehicle_data.get('hourly_price') or None,
                        status='available'  # Default holat - Mavjud
                    )
                    vehicle.save()
            except (json.JSONDecodeError, ValueError) as e:
                messages.warning(self.request, f'Mashina ma\'lumotlarida xatolik: {str(e)}')
            except Exception as e:
                # Agar plate number format noto'g'ri bo'lsa
                if 'Plate format' in str(e):
                    messages.error(self.request, f'Davlat raqami formati noto\'g\'ri: {str(e)}')
                else:
                    messages.error(self.request, f'Mashina saqlashda xatolik: {str(e)}')
                return redirect(self.request.path)
        
        # Muvaffaqiyatli xabar
        messages.success(
            self.request, 
            f'Mijoz muvaffaqiyatli qo\'shildi! '
            f'Username: {user.username}, '
            f'Parol: {generated_password}'
        )
        
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Formda xatoliklar bor. Qaytadan urinib ko\'ring.')
        return super().form_invalid(form)
