from django.shortcuts import render, redirect
from .models import Task, Group
from django.db.models import Count
from django.utils import timezone

def task_list(request):
    tasks = Task.objects.all()

    # Статистика по статусам
    stats = {
        'total': tasks.count(),
        'todo': tasks.filter(status='todo').count(),
        'doing': tasks.filter(status='progress').count(),
        'done': tasks.filter(status='done').count()
    }

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'stats': stats,
        'search_query': search_query
    })


def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.status = 'done'
    task.save()
    return redirect('task_list')
