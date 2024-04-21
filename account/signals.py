from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

"""
Considering that every new user that is created does not have a profile at first, 
I wrote this signal so that when a new user is created, a profile 
will be created for him at the same time, which is called in the app 
file with the redi method and this signal is activated.
"""
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
	if kwargs['created']:
		Profile.objects.create(user=kwargs['instance'])