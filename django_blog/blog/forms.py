from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Tag


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']


# 📝 UPDATED: Post form for creating and updating blog posts (with tags)
class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (e.g. django, python, webdev)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add tags'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your content here...'}),
        }

    def save(self, commit=True):
        """Save tags from comma-separated input."""
        post = super().save(commit=False)
        if commit:
            post.save()

        # Process tags
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]

        # Clear existing tags and re-assign
        post.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag)

        return post


# 💬 Comment form for adding/editing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }
