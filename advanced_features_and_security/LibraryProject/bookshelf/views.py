from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book, Author
from .forms import ExampleForm

# Home page (optional)
def home(request):
    return render(request, 'bookshelf/home.html')  # Make sure this template exists

# View books (requires can_view)
@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Create a book (requires can_create)
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')  # Get the author ID from the form
        author = get_object_or_404(Author, id=author_id)  # Fetch the actual Author instance
        Book.objects.create(title=title, author=author)
        return redirect('view_books')

    authors = Author.objects.all()  # Pass authors to the template for the dropdown
    return render(request, 'bookshelf/book_form.html', {'authors': authors})


# Edit a book (requires can_edit)
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_name = request.POST.get('author')  # Get author name from form
        author, created = Author.objects.get_or_create(name=author_name)
        book.author = author
        book.save()
        return redirect('view_books')
    return render(request, 'bookshelf/book_form.html', {'book': book})

# Delete a book (requires can_delete)
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('view_books')
