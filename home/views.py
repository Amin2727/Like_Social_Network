from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Post, Comment, Vote
from .forms import PostCreateUpdateForm, CommentCreateForm, CommentReplyForm

class HomeView(ListView):
	"""This view is related to our main page and pagination."""
	queryset = Post.objects.all()
	paginate_by = 4



class PostDetailView(View):
	"""
	This view is related to our detail page, which includes 
	deleting, updating, liking, commenting and replying to comments.
	"""

	form_class = CommentCreateForm
	form_class_reply = CommentReplyForm

	def setup(self, request, *args, **kwargs):
		self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
		return super().setup(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		comments = self.post_instance.pcomments.filter(is_reply=False)
		can_like = False
		if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
			can_like = True
		return render(request, 'home/detail.html', {'post':self.post_instance, 'comments':comments,
					'form':self.form_class, 'form_reply':self.form_class_reply, 'can_like':can_like})

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.user = request.user
			new_comment.post = self.post_instance
			new_comment.save()
			messages.success(request, 'your comment submitted successfully', 'success')
			return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)




class PostDeleteView(LoginRequiredMixin, View):
	"""
	This view is about deleting posts, each user can only delete her 
	own post, except for the superuser who can also delete other users's posts.
	"""

	def get(self, request, post_id):
		post = get_object_or_404(Post ,pk=post_id)
		if post.user.id == request.user.id:
			post.delete()
			messages.success(request, 'Post deleted successfully.', 'success')
		elif request.user.is_superuser:
			post.delete()
			messages.success(request, 'Post deleted successfully.', 'success')
		else:
			messages.error(request, 'You cant delete this post...!', 'danger')
		return redirect('home:home')




class PostUpdateView(LoginRequiredMixin, View):
	"""This view is related to updating posts, 
	each user can only update his own post."""
		
	form_class = PostCreateUpdateForm

	def setup(self, request, *args, **kwargs):
		self.post_instance = get_object_or_404(Post ,pk=kwargs['post_id'])
		return super().setup(request, *args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		post = self.post_instance
		if post.user.id != request.user.id and not request.user.is_superuser:
			messages.error(request, 'You cant update this post...!', 'danger')
			return redirect('home:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(instance=post)
		return render(request, 'home/update.html',{'form':form})
	
	def post(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(request.POST, instance=post)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['title'])
			new_post.user = request.user
			new_post.save()
			messages.success(request, 'You updated this post successfully.', 'success')
			return redirect('home:post_detail', post.id, post.slug)




class PostCreateView(LoginRequiredMixin, View):
	"""This view is for users to create posts."""

	form_class = PostCreateUpdateForm

	def get(self, request, *args, **kwargs):
		form = self.form_class
		return render(request, 'home/create.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['title'])
			new_post.user = request.user
			new_post.save()
			messages.success(request, 'You created a new post.', 'success')
			return redirect('home:post_detail', new_post.id, new_post.slug)
		


class PostAddReplyView(LoginRequiredMixin, View):
	"""
	This view is related to the response to the 
	comments of the users who commented on the posts.
	"""

	form_class = CommentReplyForm

	def post(self, request, post_id, comment_id):
		post = get_object_or_404(Post, id=post_id)
		comment = get_object_or_404(Comment, id=comment_id)
		form = self.form_class(request.POST)
		if form.is_valid():
			replies = form.save(commit=False)
			replies.user = request.user
			replies.post = post
			replies.reply = comment
			replies.is_reply = True
			replies.save()
			messages.success(request, 'Your reply submitted successfully', 'success')
			return redirect('home:post_detail', post.id, post.slug)
		

class PostLikeView(LoginRequiredMixin, View):
	"""This view is about liking posts by other users."""

	def get(self, request, post_id):
		post = get_object_or_404(Post, id=post_id)
		like = Vote.objects.filter(post=post, user=request.user)
		if like.exists():
			messages.error(request, 'You have already liked this post', 'danger')
		else:
			Vote.objects.create(post=post, user=request.user)
			messages.success(request, 'You liked this post', 'success')
		return redirect('home:post_detail', post.id, post.slug)
	


class PostSearchView(ListView):
	"""This view is related to searching and pagination."""

	paginate_by = 4
	template_name = "home/search_list.html"

	def get_queryset(self):
		search = self.request.GET.get('q')
		return Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['search'] = self.request.GET.get('q')
		return context