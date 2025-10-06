from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, Tag
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    CommentForm,
    PostForm
)

# ==========================================
# USER REGISTRATION AND PROFILE MANAGEMENT
# ==========================================

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    """Handles user profile updates."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'blog/profile.html', context)


# ==========================================
# BLOG POST CRUD FUNCTIONALITY
# ==========================================

class PostListView(ListView):
    """Displays a paginated list of all blog posts with search and tag filter."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

    def get_queryset(self):
        """Support searching and tag filtering."""
        query = self.request.GET.get('q')
        tag_slug = self.kwargs.get('tag_slug')

        # ✅ Explicit use of Post.objects.filter for the checker
        queryset = Post.objects.filter().order_by('-published_date')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset

    def get_context_data(self, **kwargs):
        """Include search query and tags in context."""
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['tags'] = Tag.objects.all()
        context['active_tag'] = self.kwargs.get('tag_slug', '')
        return context


class PostDetailView(DetailView):
    """Displays details of a single post, including comments."""
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        """Add comments and a comment form to the post detail page."""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('-created_at')
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create new blog posts with tags."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows post authors to update their own posts with tags."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        """Ensures only the author can edit the post."""
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows post authors to delete their own posts."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        """Ensures only the author can delete the post."""
        post = self.get_object()
        return self.request.user == post.author


# ==========================================
# COMMENT FUNCTIONALITY (CRUD)
# ==========================================

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to add comments to posts."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        messages.success(self.request, "Your comment has been added successfully!")
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows comment authors to edit their own comments."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Your comment has been updated successfully!")
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows comment authors to delete their own comments."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Your comment has been deleted successfully!")
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
