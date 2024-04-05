from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length = 50, unique=True, null = False, blank=False)
    description = models.TextField(null = True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    