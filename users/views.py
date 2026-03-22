from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from main.models import Users

def register(request):
    if request.session.get("Username"): return redirect("/Home") #Check if user is logged in
    
    if request.method == "GET": return render(request, "register.html") #Method get

    #---------------Logic--------------#

    elif request.method == "POST": #If the user posted do this
        Username = request.POST.get("username") #Get the username
        Password = request.POST.get("password") #Get the password

        if Users.objects.filter(Username=Username).first(): #Look for user in database
            messages.info(request, "Username is already in use")
            return render(request, "register.html")
        
        else:
            Users.objects.create(Username=Username, Password=make_password(Password)) #Create an user for the database with a hashed password
            messages.info(request, "Account created")
            return redirect("/Login")


def login(request):
    if request.session.get("Username"): return redirect("/Home") #Check if user is logged in

    if request.method == "GET": return render(request, "login.html") #Method get
    
    #---------------Logic--------------#
    
    elif request.method == "POST":
        Username = request.POST.get("username")
        Password = request.POST.get("password")

        Found_User = Users.objects.filter(Username=Username).first()

        if Found_User:
            if check_password(Password, Found_User.Password):
                request.session["Username"] = Username 
                return redirect("/Home")
            else:
                messages.info(request, "Wrong password or username")
                return render(request, "login.html")
            
        else:
            messages.info(request, "Wrong password or username")
            return render(request, "login.html")


def logout(request):
    request.session.pop("Username", None)
    return redirect("/Login")