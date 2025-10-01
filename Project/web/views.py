from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable

from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task


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
