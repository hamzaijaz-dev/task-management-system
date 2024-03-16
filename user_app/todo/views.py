import requests
from django.conf import settings
from django.contrib.auth import logout
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from user_app.email import CreateTodo
from .forms import UserRegistrationForm, TodoForm
from .models import Todo


@login_required
def home(request):
    """
    Create todo item and view other todo items as well.
    """
    if request.method == 'POST':
        form = TodoForm(request.POST, user=request.user)
        if form.is_valid():
            todo_data = form.cleaned_data
            todo_data['due_date'] = todo_data['due_date'].isoformat()
            todo_data['assigned_to_id'] = todo_data.get('assigned_to').id if todo_data.get('assigned_to') else 0
            todo_data['creator_id'] = request.user.id
            del todo_data['assigned_to']
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/todos/",
                json=todo_data
            )
            if response.status_code == 200:
                CreateTodo().send(recipients=[request.user.email], context={})
                return redirect("home")
    else:
        form = TodoForm(user=request.user)

    response = requests.get(
        f"{settings.FASTAPI_BASE_URL}/get_user_todos/{request.user.id}"
    )
    if response.status_code == 200:
        todos = response.json()
    else:
        todos = []


    paginator = Paginator(todos['my_todos'], 4)
    page_number = request.GET.get("my_todo")
    my_todo_page = paginator.get_page(page_number)

    paginator = Paginator(todos['assigned_todos'], 4)
    page_number = request.GET.get("assigned_todo")
    assigned_todo_page = paginator.get_page(page_number)

    context = {"form": form, "my_todos": todos, "assigned_todos": todos, "my_todo_page": my_todo_page, "assigned_todo_page": assigned_todo_page}
    return render(request, "todo/todo_app.html", context)

def register(request):
    """
    User Registration form

    Args:
        request (POST): New user registered
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {"form": form}
    return render(request, "todo/register.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")



def update_todo(request, pk):
    """
    Update todo item

    Args:
        pk (Integer): Todo ID - primary key
    """
    json_data = {
        "title": request.POST.get("title"),
        "description": request.POST.get("description"),
        "status": request.POST.get("status"),
    }
    response = requests.put(
        f"{settings.FASTAPI_BASE_URL}/todos/{pk}/",
        json=json_data
    )

    if response.status_code == 200:
        return redirect("home")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_todo(request, pk):
    """
    Delete todo item
    Args:
        pk (Integer): Todo ID - Primary key
    """
    response = requests.delete(
        f"{settings.FASTAPI_BASE_URL}/todos/{pk}/"
    )
    if response.status_code == 200:
        return redirect("home")

    return redirect("home")
