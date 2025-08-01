from django.core.paginator import Paginator
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import TaskForm
@login_required
def task_list(request):
    user = request.user
    if user.is_superuser:
        tasks = Task.objects.all().order_by('-due_date')  # Superuser sees all tasks
    else:
        tasks = Task.objects.filter(assigned_to=user).order_by('-due_date')  # Normal user: tasks assigned to them

    paginator = Paginator(tasks, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/task_list.html', {'page_obj': page_obj})



@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()

            subject = f"New Task Created: {task.title}"
            message = f"""Hi {task.assigned_to.username},

You have been assigned a new task by  {request.user.username}

Title: {task.title}
Description: {task.description}
Due Date: {task.due_date}




Login to your dashboard to manage the task.

- Task Manager
"""

            send_mail(
                subject,
                message,
                'arjavbadjate1404@gmail.com',  # Replace with your actual sender email
                [task.assigned_to.email],
                fail_silently=False,
            )

            return redirect('tracker:task_list')
    else:
        form = TaskForm()

    return render(request, 'tracker/create_task.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('tracker:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    return render(request, 'tracker/create_task.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tracker:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tracker:task_list')  # or wherever you want to land
        else:
            return render(request, 'tracker/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tracker/login.html')  # GET request


def delete_task(request , task_id):
    task = get_object_or_404(Task , id=task_id)
    task.delete()
    return redirect('tracker:task_list')
