from django.db import models


class Task(models.Model):
    caption = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", related_name="tasks")


class Tag(models.Model):
    name = models.CharField(max_length=100)
