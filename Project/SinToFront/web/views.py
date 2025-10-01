from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable
import base64
import io
import cv2
import numpy as np
import json

from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Task
# from .model.gesture_detector import GestureDetector


def home(request):
    return render(request, 'index.html')


# Dependency inversion via repository abstraction
class TaskRepository(Protocol):
    def list(self) -> Iterable[Task]:
        ...

    def create(self, title: str, description: str) -> Task:
        ...

    def update(self, task: Task, **fields) -> Task:
        ...

    def delete(self, task: Task) -> None:
        ...


class DjangoORMTaskRepository:
    def list(self) -> Iterable[Task]:
        return Task.objects.active()

    def create(self, title: str, description: str) -> Task:
        return Task.objects.create(title=title, description=description)

    def update(self, task: Task, **fields) -> Task:
        for key, value in fields.items():
            setattr(task, key, value)
        task.save()
        return task

    def delete(self, task: Task) -> None:
        task.delete()


# Strategy pattern for sorting tasks
class TaskSortStrategy(Protocol):
    def sort(self, tasks: Iterable[Task]) -> Iterable[Task]:
        ...


class SortByCreatedDesc:
    def sort(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


class SortByTitleAsc:
    def sort(self, tasks: Iterable[Task]) -> Iterable[Task]:
        return sorted(tasks, key=lambda t: t.title.lower())


@dataclass
class TaskListService:
    repo: TaskRepository
    sorter: TaskSortStrategy

    def list_tasks(self) -> Iterable[Task]:
        return self.sorter.sort(self.repo.list())


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status"]


class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        repo = DjangoORMTaskRepository()
        sort_key = self.request.GET.get("sort", "created")
        sorter: TaskSortStrategy = SortByCreatedDesc() if sort_key == "created" else SortByTitleAsc()
        service = TaskListService(repo=repo, sorter=sorter)
        return list(service.list_tasks())


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task_list")


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("task_list")


class TaskDeleteView(DeleteView):
    model = Task
    template_name = "task_confirm_delete.html"
    success_url = reverse_lazy("task_list")


@csrf_exempt
@require_http_methods(["POST"])
def detectar_gesto(request):
    try:
        # Simulación de detección de gestos para demo
        import random
        
        gestos_posibles = ["Close", "Previous", "Next", "No detectado"]
        gesto_detectado = random.choice(gestos_posibles)
        
        return JsonResponse({
            'gesto': gesto_detectado,
            'confidence': 0.85
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def get_recommendations(request):
    """Endpoint para obtener recomendaciones de música"""
    try:
        from .recommendation_system import GlobalRecommendationSystem
        
        data = json.loads(request.body)
        user_id = data.get('user_id', 1)
        strategy_type = data.get('strategy', 'hybrid')
        context = data.get('context', {})
        
        # Crear usuario mock
        class MockUser:
            def __init__(self, id):
                self.id = id
                self.username = f"user_{id}"
        
        user = MockUser(user_id)
        
        # Obtener recomendaciones
        system = GlobalRecommendationSystem()
        recommendations = system.get_recommendations(
            user, 
            strategy_type=strategy_type,
            context=context
        )
        
        return JsonResponse({
            'recommendations': recommendations,
            'strategy_used': strategy_type,
            'total_count': len(recommendations)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_preferences(request):
    """Endpoint para actualizar preferencias del usuario"""
    try:
        from .recommendation_system import GlobalRecommendationSystem
        
        data = json.loads(request.body)
        user_id = data.get('user_id', 1)
        preferences = data.get('preferences', {})
        
        # Crear usuario mock
        class MockUser:
            def __init__(self, id):
                self.id = id
                self.username = f"user_{id}"
        
        user = MockUser(user_id)
        
        # Actualizar preferencias
        system = GlobalRecommendationSystem()
        success = system.update_preferences(user, preferences)
        
        return JsonResponse({
            'success': success,
            'message': 'Preferencias actualizadas correctamente' if success else 'Error al actualizar preferencias'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

