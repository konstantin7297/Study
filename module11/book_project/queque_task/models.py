from typing import Union

from django.db import models, transaction


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

    @staticmethod
    @transaction.atomic
    def get_pending(worker_id: int) -> Union['Task', None]:
        """ Отдает задачу в статусе pending, т.е. свободную. """
        try:
            task = Task.objects.select_for_update().get(status="pending")
            task.status = "processing"
            task.worker_id = worker_id
            task.save(update_fields=["status", "worker_id"])
            return task
        except Task.DoesNotExist:
            return None
