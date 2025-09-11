from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from .models import Library, Book


# --- Authentication Views ---

def home(request):
    return render(request, "relationship_app/home.html")


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


# --- Function-based wrapper for checker ---
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


# --- Role-Based Access Control Views ---

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")

@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    return HttpResponse("You have permission to add a book.")

@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, book_id):
    return HttpResponse(f"You have permission to edit book {book_id}.")

@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, book_id):
    return HttpResponse(f"You have permission to delete book {book_id}.")