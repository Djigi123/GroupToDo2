from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'План'),
        ('progress', 'В работе'),
        ('done', 'Готово'),
    ]

    # Привязка к пользователю. null=True/blank=True оставлены для старых записей,
    # но новые будут привязываться к тебе.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_tasks',
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )

    title = models.CharField(max_length=200, verbose_name="Название задачи")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo',
        verbose_name="Статус"
    )

    # Поле дедлайна. Важно для нашей логики "Просрочено"
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Срок выполнения"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    # Поле для даты фактического выполнения (заполняется в методе save)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата завершения"
    )

    def save(self, *args, **kwargs):
        """Автоматическое управление датой завершения при смене статуса"""
        if self.status == 'done' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 'done':
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        # Сортировка по умолчанию: сначала выполненные задачи вниз,
        # а активные с ближайшим дедлайном — вверх.
        ordering = ['status', 'deadline', '-created_at']