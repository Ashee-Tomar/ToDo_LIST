from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login, logout
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

from .models import Tasks
from .form import TaskForm
from .signup_form import SignupForm

# Create your views here.
@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def welcome_page(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    task_data = Tasks.objects.filter(user=request.user).order_by('complete_status')
    completed_tasks = task_data.filter(complete_status=True).count();
    incomplete_tasks = task_data.count() - completed_tasks
    print(completed_tasks)
    context = {
        'tasks' : task_data,
        'complete__tasks' : completed_tasks,
        'incomplete_tasks' : incomplete_tasks
    }
    return render(request, 'task_list.html', context)


def delete_task(request, id):
    Tasks.objects.filter(id=id).delete()
    return redirect('home_page')

def mark_task(request, id):
    task = Tasks.objects.get(id=id)
    task.complete_status = not task.complete_status
    task.save()
    return redirect('home_page')


def add_task(request):

    form = TaskForm()

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            user = request.user
            title = form.cleaned_data['task_title']
            description = form.cleaned_data['task_description']
            data = Tasks(user=user, title=title, description=description)
            data.save()
            return redirect('home_page')

    return render(request, 'add_task.html', {'task_form':form})


def search_task(request):

    if request.user.is_authenticated:
        task_title = request.GET['searched_title']
        result = Tasks.objects.filter(user=request.user).filter(title__icontains=task_title);

    return render(request, "task_list.html", {'tasks':result})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            print("signup form valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request,'signup.html',{'form':form, 'form_error':form.errors.as_text()})

    else:
        form = SignupForm()

    return render(request,'signup.html',{'form':form})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):

    if request.user.is_authenticated:
        return redirect("home_page")

    form = AuthenticationForm(request.POST or None)
    if request.method == 'POST':
        uname = request.POST['username']
        upass = request.POST['password']
        user = authenticate(request, username=uname, password=upass)

        if user is not None:
            login(request, user=user)
            return redirect('home_page')
        else:
            err_msg = form.error_messages.get('invalid_login')
            form = AuthenticationForm(request.POST)
            return render(request,'login.html',{'form':form, 'form_error': err_msg+" "})
    
    form = AuthenticationForm(request.POST)
    return render(request,'login.html',{'form':form , 'form_error':''})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    logout(request)
    return redirect('user_login')