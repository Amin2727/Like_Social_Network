from django.db import models
from django.contrib.auth.models import User


class Relation(models.Model):
    """
    This model is related to following or unfollowing users
    """
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __srt__(self):
        return f'{self.from_user} following {self.to_user}'
    


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	age = models.PositiveSmallIntegerField(default=0)
	bio = models.TextField(null=True, blank=True)