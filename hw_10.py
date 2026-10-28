import os
from datetime import timedelta
from django.utils import timezone


import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from tasks.models import Task, SubTask, Status

# Создание записей:

task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=3),
)
print(task.id, task.title, task.status, task.deadline)


subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="New",
    deadline=timezone.now() + timedelta(days=2),
    task=task,
)

subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="New",
    deadline=timezone.now() + timedelta(days=1),
    task=task,
)

print(task.subtasks.all())


# Чтение записей:

new_tasks = Task.objects.filter(status="New")
print(new_tasks)

for t in new_tasks:
    print(t.title, t.status, t.deadline)

overdue_done = SubTask.objects.filter(
    status="Done",
    deadline__lt=timezone.now(),
)
print(overdue_done)

for st in overdue_done:
    print(st.title, st.status, st.deadline)


# Изменение записей:

task = Task.objects.get(title="Prepare presentation")
task.status = "In progress"
task.save()
print(task.title, task.status)

SubTask.objects.filter(title="Gather information").update(
    deadline=timezone.now() - timedelta(days=2)
)
print(SubTask.objects.get(title="Gather information").deadline)

SubTask.objects.filter(title="Create slides").update(
    description="Create and format presentation slides"
)
print(SubTask.objects.get(title="Create slides").description)


#Удаление записей:

task = Task.objects.get(title="Prepare presentation")
result = task.delete()
print(result)

print(Task.objects.filter(title="Prepare presentation").exists())
