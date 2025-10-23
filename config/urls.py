"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    from vehicles.models import Vehicle
    from bookings.models import Booking
    from contracts.models import Contract
    from accounts.models import CustomUser
    
    # Mijozlar statistikasi (admin emas)
    total_users = CustomUser.objects.filter(role__in=['owner', 'renter']).count()
    owner_count = CustomUser.objects.filter(role='owner').count()
    renter_count = CustomUser.objects.filter(role='renter').count()
    
    context = {
        'user': request.user,
        'total_vehicles': Vehicle.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_contracts': Contract.objects.count(),
        'total_users': total_users,
        'owner_count': owner_count,
        'renter_count': renter_count,
    }
    
    return render(request, 'accounts/dashboard.html', context)

def redirect_to_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", redirect_to_dashboard),
    path("dashboard/", dashboard, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("vehicles/", include("vehicles.urls")),
    path("contracts/", include("contracts.urls")),
    path("bookings/", include("bookings.urls")),
    path("constants/", include("constants.urls")),
]
