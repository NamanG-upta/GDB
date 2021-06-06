from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
import os


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
def startbtn(request,pk,id):
    print("idsssssssss = ", pk, id)
    user = User.objects.get(id=id)
    task = Task.objects.get(id=pk,user=user)
    task.working = True
    task.save()
    # os.system('cmd /k "dir"')
    os.system('cmd /k "cd c:\ST\STM32CubeIDE_1.6.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.stlink-gdb-server.win32_1.6.0.202101291314\tools\bin&&ST-LINK_gdbserver.exe -d -v -cp "c:\ST\STM32CubeIDE_1.6.1\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.cubeprogrammer.win32_1.6.0.202101291314\tools\bin""')


    return redirect(home)


@login_required(login_url="login")
def stopbtn(request, pk,id):
    user = User.objects.get(id=id)
    task = Task.objects.get(id=pk,user=user)
    task.working = False
    task.save()
    os.system('cmd /k "exit()"')
    return redirect(home)


@login_required(login_url="login")
def home(request):
    user = User.objects.get(id=request.user.id)

    if len(Task.objects.filter(user=user)) == 0 :
        admin_usr = User.objects.filter(is_superuser=True).first()
        tasks = Task.objects.filter(user=admin_usr)

        for curr_task in tasks:
            tsk = Task(
                title=curr_task.title,
                desc=curr_task.desc,
                complete=False,
                working=False,
                user=user,
                board_id=curr_task.board_id,
                ip_address=curr_task.ip_address
                )
            tsk.save()

        objs = Task.objects.filter(user=user)
        all_objs = Task.objects.all()
        print('2222', all_objs)
        if user.is_superuser == True:
            context = {'tasks':all_objs,'user':user}
            return render(request, "index.html", context)
        else:
            context = {'tasks':objs,'user':user}
            return render(request, "index.html", context)
    
    objs = Task.objects.filter(user=user)
    context = {'tasks':objs,'user':user}
    all_objs = Task.objects.all()
    print('outsideeeee = ', all_objs)
    if user.is_superuser == True:
        context = {'tasks':all_objs,'user':user}
        return render(request, "index.html", context)
    else:
        return render(request, "index.html", context)


@login_required(login_url="login")
def go(request):
    return render(request,"help.html")


def signup(request):
    if request.method == "POST":
        # fetching the name of the user
        name = request.POST["username"]
        institute = request.POST["institute"]
        contact = request.POST["contact"]
        email = request.POST["email"]
        name = request.POST['Name']
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
                    username=name, password=request.POST["password"],email=email,first_name=name
                )
                user.save()
                newuser = NewUser(institute_name=institute,contact=contact,user=user)
                newuser.save()
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
        user = authenticate(request,username=name,password=pas)

        # checking if user exist and credentials are correct
        if user is not None:
            if user.is_staff:
                auth.login(request, user)
                return redirect(home)
                # return render(request, "index.html")
            else:
                return render(request, "home.html", {"error": "You are not allowed to login, Please ask admin"})
        else:
            return render(request, "home.html", {"error": "Invalid Credentials"})
    else:
        return render(request, "home.html")


def logout(request):
    auth.logout(request)
    return redirect(home)