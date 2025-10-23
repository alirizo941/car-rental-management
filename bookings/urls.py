from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('<int:pk>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('<int:pk>/update-payment/', views.update_payment_status, name='update_payment_status'),
]
