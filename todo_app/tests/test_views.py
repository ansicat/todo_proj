from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from todo_app.models import Task, Tag


def create_tag(name: str = "test tag") -> Tag:
    tag = Tag.objects.create(name=name)

    return tag


def create_task(
    caption: str = "test task caption",
    completed: bool = False,
    tag_name: str = "test tag",
) -> Task:
    tag = create_tag(name=tag_name)
    task = Task.objects.create(caption=caption, completed=completed)
    task.tags.add(tag)

    return task


class TaskListViewTest(TestCase):
    def test_task_list_view_displays_task(self):
        task = create_task()
        response = self.client.get(reverse("todo-app:task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.caption)


class TaskCreateViewTest(TestCase):
    def test_task_create_view_creates_task(self):
        Tag.objects.create(name="test tag")
        data = {
            "caption": "test task caption",
            "deadline": datetime(2023, 3, 31),
            "completed": False,
            "tags": [1],
        }
        response = self.client.post(reverse("todo-app:task-create"), data=data)

        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().caption, data["caption"])


class TaskUpdateViewTest(TestCase):
    def test_task_update_view_updates_task(self):
        task = create_task(caption="test task caption")
        data = {"caption": "test task updated", "completed": True, "tags": [1]}
        response = self.client.post(
            reverse("todo-app:task-update", args=[task.pk]), data=data
        )
        task.refresh_from_db()

        self.assertEqual(task.caption, data["caption"])
        self.assertEqual(task.completed, True)


class TaskProcessViewTest(TestCase):
    def test_task_process_view_updates_task(self):
        task = create_task()
        data = {
            "completed": True,
        }
        response = self.client.post(
            reverse("todo-app:task-process", args=[task.pk]), data=data
        )
        task.refresh_from_db()

        self.assertEqual(task.completed, True)

        data = {
            "completed": False,
        }
        response = self.client.post(
            reverse("todo-app:task-process", args=[task.pk]), data=data
        )
        task.refresh_from_db()

        self.assertEqual(task.completed, False)


class TaskDeleteViewTest(TestCase):
    def test_task_delete_view_deletes_task(self):
        task = create_task()

        self.assertEqual(Task.objects.filter(pk=task.pk).count(), 1)
        response = self.client.post(
            reverse("todo-app:task-delete", args=[task.pk])
        )
        self.assertEqual(Task.objects.filter(pk=task.pk).count(), 0)


class TagListViewTest(TestCase):
    def test_tag_list_view_displays_tag(self):
        tag = create_tag()
        response = self.client.get(reverse("todo-app:tag-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, tag.name)


class TagCreateViewTest(TestCase):
    def test_tag_create_view_creates_tag(self):
        data = {"name": "test tag"}
        response = self.client.post(reverse("todo-app:tag-create"), data=data)

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.first().name, data["name"])

    def test_tag_create_view_creates_tag_without_name(self):
        data = {}
        response = self.client.post(reverse("todo-app:tag-create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "name",
                             "This field is required.")
        self.assertEqual(Tag.objects.all().count(), 0)

    def test_create_tag_with_duplicate_name(self):
        create_tag(name="test tag")

        data = {"name": "test tag"}
        response = self.client.post(reverse("todo-app:tag-create"), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "name",
                             "Tag with this Name already exists.")
        self.assertEqual(Tag.objects.all().count(), 1)


class TagUpdateViewTest(TestCase):
    def test_tag_update_view_updates_tag(self):
        tag = create_tag(name="test tag")
        data = {"name": "test tag updated"}
        response = self.client.post(
            reverse("todo-app:tag-update", args=[tag.pk]), data=data
        )
        tag.refresh_from_db()

        self.assertEqual(tag.name, data["name"])


class TagDeleteViewTest(TestCase):
    def test_tag_delete_view_deletes_tag(self):
        tag = create_tag()

        self.assertEqual(Tag.objects.filter(pk=tag.pk).count(), 1)
        response = self.client.post(
            reverse("todo-app:tag-delete", args=[tag.pk])
        )
        self.assertEqual(Tag.objects.filter(pk=tag.pk).count(), 0)
