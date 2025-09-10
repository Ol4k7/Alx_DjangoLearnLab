from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication views using the custom views
    path("login/", views.CustomLoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", views.CustomLogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
