from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *


@login_required(login_url="login")
def updateTask(request, pk):
    user = User.objects.get(id=request.user.id)
    task = Task.objects.get(id=pk,user=user)

    if request.method == 'POST':
        task = Task.objects.get(id=pk,user=user)
        task.complete = True
        task.save()
        return redirect(home)

    return render(request, 'update_task.html', {'task':task} )


@login_required(login_url="login")
def home(request):
    user = User.objects.get(id=request.user.id)

    if len(Task.objects.filter(user=user)) == 0 :
        all_users = User.objects.all()
        admin_usr = -1

        for curr_user in all_users:
            if curr_user.is_superuser:
                admin_usr = curr_user
        
        tasks = Task.objects.filter(user=admin_usr)

        for curr_task in tasks:
            tsk = Task(
                title=curr_task.title,
                desc=curr_task.desc,
                complete=False,
                user=user,
                board_id=curr_task.board_id,
                ip_address=curr_task.ip_address
                )
            tsk.save()

        objs = Task.objects.filter(user=user)
        context = {'tasks':objs,'user':user}
        return render(request, "index.html", context)
    
    objs = Task.objects.filter(user=user)
    context = {'tasks':objs,'user':user}
    return render(request, "index.html", context)


def signup(request):
    if request.method == "POST":
        # fetching the name of the user
        name = request.POST["username"]
        if request.POST["password"] == request.POST["passwordagain"]:
            # if passwords matched check if user exist previously or not
            try:
                # user already exist
                user = User.objects.get(username=name)
                return render(
                    request,
                    "register.html",
                    {"error": "Username has Already been Taken", "user": user},
                )
            except User.DoesNotExist:
                # create a user and redirect to home
                user = User.objects.create_user(
                    username=name, password=request.POST["password"]
                )
                return redirect(home)
        else:
            return render(
                request, "register.html", {"error": "Passwords Don't Matched"}
            )
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        name = request.POST["username"]
        pas = request.POST["password"]
        user = auth.authenticate(username=name, password=pas)

        # checking if user exist and credentials are correct
        if user is not None:
            auth.login(request, user)
            return redirect(home)
        else:
            return render(request, "home.html", {"error": "Invalid Credentials"})
    else:
        return render(request, "home.html")


def logout(request):
    auth.logout(request)
    return redirect(home)