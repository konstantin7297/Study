from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.request import Request

from queque_task.models import Task


def worker_process(task: Task) -> Task:
    """ Рабочий процесс """
    task.status = "completed"
    task.save(update_fields=["status"])
    return task


@api_view(['GET'])  # Задача 6 из модуля 13.
@renderer_classes([JSONRenderer])
def fetch_task(request: Request, worker_id: int, create_task: bool = True) -> Response:
    """ Функция для отдачи задачи на worker. """
    try:
        if create_task:
            Task.objects.get_or_create(task_name="task1", status="pending")

        task = Task.get_pending_task(worker_id)
        return Response({"result": str(worker_process(task).status)})
    except Task.DoesNotExist:
        return Response({"result": "Нет задач."})
