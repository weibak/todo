from django.conf import settings
from django.db import models


class Note(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="note"
    )
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )


class Tags(models.Model):
    title = models.CharField(max_length=200)
    note = models.ManyToManyField(Note)
