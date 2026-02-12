from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


@login_required
def login_redirect(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    return redirect('task_list')


@login_required
def task_list(request):
    # Сортируем: сначала те, у которых дедлайн ближе
    tasks = Task.objects.filter(user=request.user).order_by('deadline', 'created_at')

    # Фильтрация по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    stats = {
        'total': Task.objects.filter(user=request.user).count(),
        'todo': Task.objects.filter(user=request.user, status='todo').count(),
        'doing': Task.objects.filter(user=request.user, status='progress').count(),
        'done': Task.objects.filter(user=request.user, status='done').count(),
    }

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'stats': stats,
        'search_query': search_query,
        'now': timezone.now()  # Для проверки просрочки в HTML
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        deadline = request.POST.get('deadline')
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                deadline=deadline if deadline else None
            )
    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = 'done'
    task.save()  # completed_at заполнится автоматически в модели
    return redirect('task_list')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_redirect')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})