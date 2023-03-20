from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from todo_app.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    queryset = Task.objects.order_by(
        "completed", "-created"
    ).prefetch_related()


class TaskCreateView(generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy("todo-app:task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = "__all__"
    template_name = "todo_app/task_form.html"
    success_url = reverse_lazy("todo-app:task-list")


class TaskProcessView(View):
    def post(self, request, pk):
        state = request.POST.get("completed")

        if state == "True":
            Task.objects.filter(pk=pk).update(completed=True)

        if state == "False":
            Task.objects.filter(pk=pk).update(completed=False)

        return redirect("todo-app:task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "todo_app/task_delete.html"
    success_url = reverse_lazy("todo-app:task-list")


class TagListView(generic.ListView):
    model = Tag
    queryset = Tag.objects.order_by("name")


class TagCreateView(generic.CreateView):
    model = Tag
    fields = "__all__"
    template_name = "todo_app/tag_form.html"
    success_url = reverse_lazy("todo-app:tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = "__all__"
    template_name = "todo_app/tag_form.html"
    success_url = reverse_lazy("todo-app:tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    template_name = "todo_app/tag_delete.html"
    success_url = reverse_lazy("todo-app:tag-list")
