# LibraryProject/bookshelf/forms.py

from django import forms
from .models import Book, Author

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)