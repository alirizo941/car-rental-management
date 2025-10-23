from django.urls import path
from . import views

urlpatterns = [
    path('', views.constants_list, name='constants_list'),
]
