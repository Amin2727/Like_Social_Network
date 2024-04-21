from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    """This form is for creating or updating posts."""
    class Meta:
        model = Post
        fields = ('title', 'body')



class CommentCreateForm(forms.ModelForm):
    """This form is for creating post comments."""
    class Meta:
        model = Comment
        fields =('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Put your comment...'})
        }


class CommentReplyForm(forms.ModelForm):
    """This form is for replying to post comments."""
    class Meta:
        model= Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Put your Reply...'})
        }