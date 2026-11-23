from django.conf import settings
from django.core.mail import send_mail
from django.tasks import task

from tasks.models import Task


@task
def send_email_task_status(task_id, old_status, new_status):
    task_obj = Task.objects.select_related('owner').get(pk=task_id)
    send_mail(
        subject=f"Task {task_obj.title}: status changed",
        message=f"Hello {task_obj.owner.username}! Your task {task_obj.title} "
                f"changed status from {old_status} to {new_status}. "
                f"Deadline {task_obj.deadline:%d/%m/%Y}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[task_obj.owner.email],
    )