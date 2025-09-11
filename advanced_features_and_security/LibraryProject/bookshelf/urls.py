from django.urls import path
from . import views

urlpatterns = [
    # add your app URLs here, e.g.
    path('', views.home, name='home'),
    path('books/', views.view_books, name='view_books'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]
