"""doacoes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='main_page'), name='index'),
    path('main_page/', views.main_page, name='main_page'),
    path('cadastrar_doador/', views.cadastrar_doador, name='cadastrar_doador'),
    path('editar_doador/<int:doador_id>/', views.editar_doador, name='editar_doador'),
    path('excluir_doador/<int:doador_id>/', views.excluir_doador, name='excluir_doador'),
    path('pesquisar_doador/', views.pesquisar_doador, name='pesquisar_doador'),
    path('reativar_doador/<int:doador_id>/', views.reativar_doador, name='reativar_doador'),
]
