import time
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .models import Todo

_start = time.time()


def home(request):
    """Main todo list view."""
    todos = Todo.objects.all()
    return render(request, 'api/index.html', {'todos': todos})


@require_http_methods(["POST"])
def todo_create(request):
    """Create a new todo item."""
    title = request.POST.get('title', '').strip()
    if title:
        Todo.objects.create(title=title)
    return redirect('home')


@require_http_methods(["POST"])
def todo_toggle(request, pk):
    """Toggle a todo item's completed status."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save(update_fields=['completed', 'updated_at'])
    return redirect('home')


@require_http_methods(["POST"])
def todo_delete(request, pk):
    """Delete a todo item."""
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('home')


def health(request):
    """Health check endpoint for load balancer / verify stage."""
    return JsonResponse({'status': 'ok', 'uptime': round(time.time() - _start, 1)})
