from django.urls import path
from django.shortcuts import render
from .views import (
    home,
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    detectar_gesto,
    get_recommendations,
    update_preferences,
)

def login_view(request):
    return render(request, 'login.html')

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('detectar-gesto/', detectar_gesto, name='detectar_gesto'),
    path('api/recommendations/', get_recommendations, name='get_recommendations'),
    path('api/preferences/', update_preferences, name='update_preferences'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/new/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
