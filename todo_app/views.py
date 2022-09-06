from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login, logout

from .models import Tasks
from .form import TaskForm
from .signup_form import SignupForm

# Create your views here.
def welcome_page(request):
    if not request.user.is_authenticated:
        return redirect("user_login")

    task_data = Tasks.objects.filter(user=request.user)
    print(task_data)
    context = {
        'tasks' : task_data,
    }
    return render(request, 'home.html', context)

# def show_task(request, id):
#     task = Tasks.objects.get(id=id)
#     context = {
#         'requested_task' : task,
#     }
#     return render(request, 'task_details.html', context)

def delete_task(request, id):
    Tasks.objects.filter(id=id).delete()
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
            return render(request,'signup.html',{'form':form, 'form_error':form.errors.as_text(),})

    else:
        form = SignupForm()

    return render(request,'signup.html',{'form':form})


def user_login(request):

    if request.method == 'POST':
        uname = request.POST['username']
        upass = request.POST['password']
        user = authenticate(request, username=uname, password=upass)

        if user is not None:
            login(request, user=user)
            return redirect('home_page')
        else:
            form = AuthenticationForm(request.POST)
            return render(request,'login.html',{'form':form})
    
    form = AuthenticationForm(request.POST)
    return render(request,'login.html',{'form':form})


def user_logout(request):
    logout(request)
    return redirect('user_login')