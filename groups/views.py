from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Users, Groups, Posts
from main.views import require_user
from django.http import Http404, FileResponse
import os

PlaceHolder = []

def download_post(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
        filepath = post.File.path
        filename = os.path.basename(filepath)
        return FileResponse(
            open(filepath, 'rb'),
            as_attachment=True,      # Force download
            filename=filename        # Suggested file name
        )
    except Posts.DoesNotExist:
        raise Http404("File not found")

def GroupHome(request, id):
    user = require_user(request)
    if not isinstance(user, Users):
        return user

    Found_Group = Groups.objects.filter(id=id).first()
    if not Found_Group: return render(request, "NotFound.html")

    for group in user.Groups: #Check if user is on group
        if group["id"] == id and group["Name"] == Groups.objects.filter(id=id).first().Name:
            break
    else:
        messages.info(request, "You are not in that group!")
        return redirect("/Home")

    posts = []
    for post in Posts.objects.filter(Group=Found_Group):
        if post.File and os.path.exists(post.File.path):
            posts.append(post)

    if request.method == "POST":
        file = request.FILES.get("file")
        message = request.POST.get("text")

        if message:
            if Found_Group.CanAnyonePost: #If anyone can post
                Found_Group.Messages.append({"Message":message, "By":user.Username})
                Found_Group.save()
                messages.info(request, "Message posted")
                return redirect(f"/Group/{id}")
            
            if user.Username in Found_Group.Admins:
                Found_Group.Messages.append({"Message":message, "By":user.Username})
                Found_Group.save()
                messages.info(request, "Message posted")
                return redirect(f"/Group/{id}")
            else:
                messages.info(request, "You can't post")
                return redirect(f"/Group/{id}")

        if file and not Posts.objects.filter(Group=Found_Group, File=file.name).exists():
            Posts.objects.create(Group=Found_Group, File=file)
            messages.info(request, "File uploaded")
        else:
            messages.warning(request, "File already exists")
        return redirect(f"/Group/{id}")

    
    return render(request, "GroupHome.html", {"id":id, "posts":posts, "Texts":Found_Group.Messages})


def LeaveGroup(request, id):
    user = require_user(request)
    if not isinstance(user, Users):
        return user
    
    Group = Groups.objects.filter(id=id).first()
    if not Group: return render(request, "NotFound.html")

    for group in user.Groups: #Check if user is on group
        if group["id"] == id and group["Name"] == Groups.objects.filter(id=id).first().Name:
            break
    else:
        messages.info(request, "You are not in that group!")
        return redirect("/Home")
    
    # Remove the group from user's JSONField
    user.Groups = [g for g in user.Groups if g.get("id") != Group.id]
    user.save()

    Group.Members = [m for m in Group.Members if m.get("id") != user.id]

    # Remove the user from Admins (if needed)
    Group.Admins = [a for a in Group.Admins if a.get("id") != user.id]

    Group.save()

    messages.info(request, "Left group")
    return redirect("/Home")