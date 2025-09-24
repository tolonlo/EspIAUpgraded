from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('home/', views.home, name='home'),
    path('canciones/', views.lista_canciones, name='lista_canciones'),
    path('login/', views.login, name='login'),
    path('terminos/', views.terminos, name='terminos'), 
    path("detectar-gesto/", views.detectar_gesto, name="detectar_gesto"),
]
