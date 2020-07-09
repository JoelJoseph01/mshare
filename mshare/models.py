from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Share(models.Model):
    author=models.CharField(max_length=30)
    title=models.CharField(max_length=50)
    content=models.TextField()
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Friends(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner',on_delete=models.CASCADE,null=True)

    @classmethod
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user = current_user

        )
        if current_user != new_friend:
            friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user,new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)