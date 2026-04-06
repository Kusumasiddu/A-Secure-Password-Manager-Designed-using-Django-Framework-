# pw_storage/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User


class Password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passwords')
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='password_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # Updated or Deleted
    password_name = models.CharField(max_length=200)  # Which password
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.password_name}"

