from django.db import models

# Author model represents a writer who can have multiple books.
# One author → Many books (One-to-Many relationship).
class Author(models.Model):
    name = models.CharField(max_length=100)  # Store the author's name

    def __str__(self):
        return self.name


# Book model represents a book written by an author.
# Each book has a title, year of publication, and a foreign key link to an Author.
class Book(models.Model):
    title = models.CharField(max_length=200)  # Title of the book
    publication_year = models.IntegerField()  # Year the book was published
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # allows accessing all books of an author via author.books.all()
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
