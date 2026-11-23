import logging

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from tasks.models import Task
from tasks.utils import send_email_task_status

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Task, dispatch_uid="task_pre_save_status")
def remember_old_status(sender, instance, raw, **kwargs):
    if raw:
        return
    if instance.pk:
        instance._old_status = (
            Task.objects.filter(pk=instance.pk)
            .values_list('status', flat=True)
            .first()
        )
    else:
        instance._old_status = None


@receiver(post_save, sender=Task, dispatch_uid="task_post_save_status")
def task_status_changed(sender, instance, created, raw, **kwargs):
    if raw or created:
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status is None or old_status == instance.status:
        return

    if instance.owner is None or not instance.owner.email:
        logger.info(f"Task {instance.pk}: owner has no email, notification skipped")
        return

    logger.info(f"Task {instance.pk}: status changed {old_status} -> {instance.status}")
    send_email_task_status.enqueue(
        task_id=instance.pk,
        old_status=old_status,
        new_status=instance.status,
    )