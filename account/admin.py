from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')


class ProfileInline(admin.StackedInline):
	"""
	I wrote this class to add the profile model that I created in the models.py file to the end of the add users 
	section in the admin panel and And the class below is a continuation of this class.
	"""
	model = Profile
	can_delete = False


class ExtendedUserAdmin(UserAdmin):
	inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)
