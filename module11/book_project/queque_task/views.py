from django.db import transaction
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.request import Request

from queque_task.models import Task


def worker_process(task: Task) -> Task:
    """ Рабочий процесс """
    try:
        task.status = "completed"
    except Exception:
        task.status = "pending"
    finally:
        task.save(update_fields=["status"])
        return task


@api_view(['GET'])
@renderer_classes([JSONRenderer])
@transaction.atomic
def fetch_task(request: Request, worker_id: int, create_task: bool = True) -> Response:
    """ Функция для отдачи задачи на worker. """
    if create_task:
        Task.objects.get_or_create(task_name="task1", status="pending")

    pending_tasks = Task.objects.filter(status="pending")

    if pending_tasks.exists():
        task = pending_tasks.first()
        task.status = "processing"
        task.worker_id = worker_id
        task.save(update_fields=["status", "worker_id"])
        return Response({"result": str(worker_process(task).status)})

    else:
        return Response({"result": "Нет задач."})
