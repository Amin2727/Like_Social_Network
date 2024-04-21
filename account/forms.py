from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegistrationForm(forms.Form):
	"""This form is related to user registration on our site."""
	
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'For Example Lars'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'name@gmail.com'}))
	password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Use Strong Password'}))
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Retype Your Password'}))

	def clean_email(self):
		"""
		This method is so that the user does not enter an 
		email that has already been registered on the site.
		"""

		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('This email already exists...!')
		return email

	def clean(self):
		"""
		This method compares two passwords entered by the user, 
		and if they are not the same, it gives an error.
		"""
		cd = super().clean()
		p1 = cd.get('password1')
		p2 = cd.get('password2')

		if p1 and p2 and p1 != p2:
			raise ValidationError('Password must match...!')




class UserLoginForm(forms.Form):
	"""This form is for users to enter the site."""

	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))




class EditUserForm(forms.ModelForm):
	"""This form is for editing or changing user specific information."""
	
	email = forms.EmailField()

	class Meta:
		model = Profile
		fields = ('age', 'bio')