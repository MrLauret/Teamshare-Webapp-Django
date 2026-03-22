from django.shortcuts import render, redirect
from .models import Users, Groups
from django.contrib import messages

#---------------Middleware--------------#
def get_logged_user(request):
    username = request.session.get("Username")

    if not username: return None
    else: return Users.objects.filter(Username=username).first()


def require_user(request):
    user = get_logged_user(request)

    if not user:
        if request.session.get("Username"):
            return render(request, "NoUser.html") #Si no está en la database
        return redirect("/Login") #Si no está logueado
    return user

#---------------Views--------------#
def custom_404(request, exception):
    return render(request, "404.html", status=404)

def home(request):
    user = require_user(request)
    if not isinstance(user, Users): #Mira si user es de la clase Users
        return user

    in_group = bool(user.Groups)
    
    return render(request,  "home.html", {
        "inGroup":in_group,
        "Groups": user.Groups if in_group else None,
        "Username":user.Username,
        })


def blank(request):
    user = get_logged_user(request)
    return redirect("/Home" if user else "/Login")

def make(request):
    user = require_user(request)
    if not isinstance(user, Users):
        return user

    #---------------Get--------------#
    if request.method == "GET":
        return render(request, "make.html")

    #---------------Post--------------#
    GroupName = request.POST.get("GroupName")

    New_Group = Groups.objects.create(
        Name=GroupName,
        Admins=[{"Username":user.Username, "id":user.id}],
        Members=[{"Username":user.Username, "id":user.id}],
    )

    user.Groups.append({"Name":GroupName, "id":New_Group.id})
    user.save()

    messages.info(request, "Group Created!")
    return redirect("/Home")

def join(request):
    user = require_user(request)
    if not isinstance(user, Users):
        return user

    #---------------Get--------------#
    if request. method == "GET":
        return render(request, "join.html")
    
    #---------------Post--------------#
    Raw_Group_Id = request.POST.get("GroupId")

    try:
        GroupId = int(Raw_Group_Id)
    except ValueError:
        messages.info(request, "No a group id, only numbers are allowed")
        return redirect("/Join")
    
    Found_Group = Groups.objects.filter(id=GroupId).first()

    if not Found_Group:
        messages.info(request, "No group found")
        return redirect("/Join")
    
    if any(group["id"] == Found_Group.id for group in user.Groups):
        messages.info(request, "You are in that group!")
        return redirect("/Join")


    user.Groups.append({"Name":Found_Group.Name, "id":Found_Group.id})
    user.save()

    Found_Group.Members.append({"Username":user.Username, "id":user.id})
    Found_Group.save()

    messages.info(request, "Joined group")
    return redirect("/Home")