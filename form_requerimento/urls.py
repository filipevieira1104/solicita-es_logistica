from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autenticacao/', include('autenticacao.urls')),
    path('solicitacao/', include('solicitacao.urls')), 
    path('recebimento/', include('recebimento.urls')),
    path("", lambda request: redirect('/autenticacao/login/')),
]
