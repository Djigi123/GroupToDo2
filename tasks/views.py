from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Project
from django.db.models import Q

def task_list(request):
    tasks = Task.objects.all().order_by('deadline')
    projects = Project.objects.all()

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query))

    # Статистика
    stats = {
        'total': tasks.count(),
        'todo': tasks.filter(status='todo').count(),
        'doing': tasks.filter(status='doing').count(),
        'done': tasks.filter(status='done').count(),
    }

    return render(request, 'tasks/index.html', {
        'tasks': tasks,
        'projects': projects,
        'stats': stats,
        'search_query': search_query
    })

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = 'done'
    task.save()
    return redirect('task_list')