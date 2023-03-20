from django.db import models


class Task(models.Model):
    caption = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", blank=True, related_name="tasks")

    def __str__(self):
        return self.caption


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
