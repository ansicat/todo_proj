from django.contrib import admin
from django.contrib.auth.models import Group

from todo_app.models import Task, Tag

admin.site.register(Task)
admin.site.register(Tag)

admin.site.unregister(Group)
