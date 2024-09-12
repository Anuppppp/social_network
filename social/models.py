from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class FriendRequest(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)


