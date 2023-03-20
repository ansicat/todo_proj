from datetime import datetime
from django.test import TestCase

from todo_app.models import Tag, Task


class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="test tag name")

    def test_tag_str(self):
        self.assertEqual(str(self.tag), "test tag name")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "test tag name")


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="test tag name")
        self.task = Task.objects.create(
            caption="test task caption",
            deadline=datetime(2023, 3, 31),
        )
        self.task.tags.set([self.tag])

    def test_task_str(self):
        self.assertEqual(str(self.task), "test task caption")

    def test_task_creation(self):
        self.assertEqual(self.task.caption, "test task caption")
        self.assertEqual(self.task.deadline, datetime(2023, 3, 31))
        self.assertFalse(self.task.completed)
        self.assertEqual(list((self.tag,)), list(self.task.tags.all()))
