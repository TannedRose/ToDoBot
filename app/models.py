import hashlib, secrets, time

import threading

import pytz

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import send_task_reminder

from datetime import datetime, timedelta


def generate_pk():
    raw = secrets.token_bytes(16) + str(time.time()).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=100, blank=True, null=True)


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=16, default=generate_pk, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=16, default=generate_pk, editable=False)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


def delayed_schedule_reminder(instance):
    try:
        TIME_ZONE = "America/Adak"
        local_tz = pytz.timezone(TIME_ZONE)

        if isinstance(instance.due_date, str):
            due_str = instance.due_date
            due = datetime.fromisoformat(due_str)
        else:
            due = instance.due_date

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

    except Exception as e:
        print(f"❌ Ошибка планирования задачи: {e}")
        print(e.args)


@receiver(post_save, sender=Task)
def schedule_task_reminder(sender, instance, created, **kwargs):
    if created:
        threading.Thread(target=delayed_schedule_reminder, args=(instance,), daemon=True).start()

