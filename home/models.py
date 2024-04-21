from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField


class Post(models.Model):
	"""This model is for showing user posts."""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
	title = models.CharField(max_length=100, null=True, blank=True)
	body = RichTextField(config_name='myconfig')
	slug = models.SlugField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering=['-created']

	def __str__(self):
		return f'{self.slug} - {self.updated}'
	
	def get_absolute_url(self):
		return reverse('home:post_detail', args=(self.id, self.slug))
	
	def likes_count(self):
		"""This method is for counting the number of likes of users' posts."""
		return self.pvotes.count()
	
	def user_can_like(self, user):
		"""
        The purpose of this method is to disable the 
        like button when a user likes another user's post.
        """

		user_like = user.uvotes.filter(post=self)
		if user_like.exists():
			return True
		return False




class Comment(models.Model):
	"""This model is for put comments on posts."""

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
	reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
	is_reply = models.BooleanField(default=False)
	body = models.TextField(max_length=400)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user} - {self.body[:20]}'



class Vote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')
	
	def __str__(self):
		return f'{self.user} likes {self.post.title}'