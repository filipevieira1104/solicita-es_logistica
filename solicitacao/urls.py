from django.urls import path
from . import views

urlpatterns = [
    path('pedido/', views.pedido, name='pedido'),
    path('atualizar_status/', views.atualizar_status, name='atualizar_status'),
]