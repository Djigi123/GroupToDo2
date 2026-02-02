from django.contrib import admin
from .models import Group, Task


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'group', 'assigned_to', 'deadline', 'created_at')
    list_filter = ('status', 'priority', 'group')
    search_fields = ('title', 'description', 'group__name', 'assigned_to__username')
    ordering = ('-created_at',)
    date_hierarchy = 'deadline'
