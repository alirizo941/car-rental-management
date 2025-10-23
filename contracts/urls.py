from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContractListView.as_view(), name='contract_list'),
    path('create/', views.ContractCreateView.as_view(), name='contract_create'),
    path('<int:pk>/', views.contract_detail, name='contract_detail'),
    path('<int:pk>/edit/', views.ContractUpdateView.as_view(), name='contract_update'),
    path('<int:pk>/delete/', views.ContractDeleteView.as_view(), name='contract_delete'),
    path('<int:pk>/toggle-status/', views.toggle_contract_status, name='toggle_contract_status'),
]
