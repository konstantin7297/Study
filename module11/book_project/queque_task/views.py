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


@api_view(['GET'])  # Задача 6 из модуля 13.
@renderer_classes([JSONRenderer])
def fetch_task(request: Request, worker_id: int, create_task: bool = True) -> Response:
    """ Функция для отдачи задачи на worker. """
    try:
        if create_task:  # Заглушка на создание задачи.
            Task.objects.get_or_create(task_name="task1", status="pending")

        if task := Task.get_pending(worker_id):  # Попытка получить задачу.
            return Response({"result": str(worker_process(task).status)})

    except Task.DoesNotExist:
        return Response({"result": "Нет задач."})
