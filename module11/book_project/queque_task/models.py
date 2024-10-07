from django.db import models


class Task(models.Model):
    """ Модель для таблицы очереди задач """
    task_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("completed", "Completed"),
        ],
        default="pending",
    )
    worker_id = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
