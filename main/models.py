from django.db import models

class Users(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    Username = models.CharField(unique=True)
    Password = models.CharField()

    Groups = models.JSONField(default=list)

    def __str__(self):
        return self.Username


class Groups(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    Name = models.CharField(max_length=50)

    Members = models.JSONField(default=list)
    Admins = models.JSONField(default=list)

    Messages = models.JSONField(default=list)

    def __str__(self):
        return self.Name

def upload_path(instance, filename):
    return f"Uploads/{instance.Group.id}/{filename}"

class Posts(models.Model):
    id = models.BigAutoField(primary_key=True)
    Group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name="posts")
    File = models.FileField(upload_to=upload_path)