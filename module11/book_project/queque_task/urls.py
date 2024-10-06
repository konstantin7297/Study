from django.urls import path

from queque_task.views import fetch_task

urlpatterns = [
    path('fetch_task/<int:worker_id>/', fetch_task, name='fetch-task'),
]
