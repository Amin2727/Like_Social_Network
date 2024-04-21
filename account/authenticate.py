from django.contrib.auth.models import User


class EmailBackend:
	"""
	By writing this class, we can log in with email.
	We need to add it to the authentication backends in the settings.py.
	"""
	def authenticate(self, request, username=None, password=None):
		try:
			user = User.objects.get(email=username)
			if user.check_password(password):
				return user
			return None
		except User.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None