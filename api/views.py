from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
from .models import Task


@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks = list(Task.objects.values())
        return JsonResponse(tasks, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.create(
            title=data.get('title'),
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        }, status=201)


@csrf_exempt
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed
        })

    if request.method == 'PUT':
        data = json.loads(request.body)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        task.save()
        return JsonResponse({'message': 'updated'})

    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'deleted'})
