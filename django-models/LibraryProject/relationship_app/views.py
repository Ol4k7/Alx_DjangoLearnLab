from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from .models import Library, Book

# --- Home View ---
def home(request):
    return render(request, "relationship_app/home.html")


# --- Authentication Views ---
class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"


class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"

    # Allow GET requests to log out (instead of only POST)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "relationship_app/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, "relationship_app/register.html", {"form": form})


# Function-based wrapper for checker compatibility
def register(request):
    view = RegisterView.as_view()
    return view(request)


# --- Book & Library Views ---

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view for library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
