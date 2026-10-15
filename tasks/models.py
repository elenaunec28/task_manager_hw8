from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name'),
        ]

class Status(models.TextChoices):
    NEW = 'New', 'New'
    IN_PROGRESS = 'In progress', 'In progress'
    PENDING = 'Pending', 'Pending'
    BLOCKED = 'Blocked', 'Blocked'
    DONE = 'Done', 'Done'

class Task(models.Model):
    title = models.CharField(max_length=200, unique_for_date='deadline')
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='tasks')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_task_title'),
        ]


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title'),
        ]
