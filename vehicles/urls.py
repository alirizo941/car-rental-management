from django.urls import path
from . import views

urlpatterns = [
    # Vehicle URLs
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    
    # CarMake URLs
    path('makes/', views.CarMakeListView.as_view(), name='carmake_list'),
    path('makes/create/', views.CarMakeCreateView.as_view(), name='carmake_create'),
    
    # CarModel URLs
    path('models/', views.CarModelListView.as_view(), name='carmodel_list'),
    path('models/create/', views.CarModelCreateView.as_view(), name='carmodel_create'),
    
    # AJAX URLs
    path('ajax/get-models/', views.get_models_by_make, name='get_models_by_make'),
]
