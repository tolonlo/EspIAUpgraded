from django.db import models
from django.utils import timezone


class TaskQuerySet(models.QuerySet):
    def active(self):
        return self.exclude(status=Task.Status.ARCHIVED)

    def by_status(self, status: str):
        return self.filter(status=status)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def by_status(self, status: str):
        return self.get_queryset().by_status(status)


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "To Do"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        DONE = "DONE", "Done"
        ARCHIVED = "ARCHIVED", "Archived"

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"

