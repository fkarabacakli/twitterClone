from django.forms import ModelForm
from .models import Post,Comment,Follow


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text',)

class FollowForm(ModelForm):
    class Meta:
        model = Follow
        fields = ('follower',)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

