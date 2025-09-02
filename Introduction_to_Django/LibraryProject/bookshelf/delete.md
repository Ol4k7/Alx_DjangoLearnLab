# Delete Operation

```python
# Import the Book model
from bookshelf.models import Book

# Retrieve the book instance to delete
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()

# Confirm deletion
Book.objects.all()  # <QuerySet []>
