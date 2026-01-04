from django.db import models
from django.contrib.auth.models import User

# а. Проекты и команды
class Project(models.Model):
    name = models.CharField(max_length=100)
    # Связь "многие-ко-многим" для команд
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name

# б, в, г. Задачи, Назначение, Статусы и Дедлайны
class Task(models.Model):
    # Варианты статусов (workflow)
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ]
    # Варианты приоритетов
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    # Назначение задачи пользователю
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    # Срок выполнения (deadline)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title