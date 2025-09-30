from datetime import datetime

import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Task
from tasks import send_task_reminder

@receiver(post_save, sender=Task)
def schedule_task_reminder(sender, instance, created, **kwargs):
    if created:
        TIME_ZONE = "America/Adak"
        local_tz = pytz.timezone(TIME_ZONE)

        due = instance.due_date
        if isinstance(due, str):
            due = datetime.fromisoformat(due)

        if due.tzinfo is None:
            due = local_tz.localize(due)
        else:
            due = due.astimezone(local_tz)

        now = datetime.now(local_tz)
        delay = max((due - now).total_seconds(), 0)

        send_task_reminder.apply_async(
            args=[instance.user.id, instance.title, due.isoformat()],
            countdown=delay
        )
