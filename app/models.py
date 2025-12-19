import hashlib, secrets, time

from django.db import models


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
