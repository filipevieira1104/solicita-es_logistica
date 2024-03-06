from django.urls import path
from . import views

urlpatterns = [
    path('recebido/', views.recebido, name='recebido'),
]
