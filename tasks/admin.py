from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Поля, которые будут видны в общем списке (таблице)
    list_display = ('title', 'user', 'status', 'deadline', 'completed_at', 'created_at')

    # Поля, по которым можно фильтровать задачи (правая колонка)
    list_filter = ('status', 'user', 'deadline', 'created_at')

    # Поля, по которым работает поиск (сверху)
    # user__username позволяет искать по имени пользователя, а не по его ID
    search_fields = ('title', 'user__username')

    # Позволяет редактировать статус прямо из общего списка, не заходя внутрь задачи
    list_editable = ('status',)

    # Добавляет удобную навигацию по датам сверху
    date_hierarchy = 'deadline'

    # Поля, которые нельзя редактировать вручную (дата создания заполняется сама)
    readonly_fields = ('created_at', 'completed_at')

    # Группировка полей внутри самой задачи для красоты
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'title', 'status')
        }),
        ('Сроки и выполнение', {
            'fields': ('deadline', 'completed_at', 'created_at')
        }),
    )