from rest_framework import serializers
from django.utils.timezone import now
from .models import Author, Book


# Serializer for Book model
# Converts Book instances to JSON and validates input when creating/updating.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # include all model fields

    # Custom validation to prevent setting a publication_year in the future
    def validate_publication_year(self, value):
        current_year = now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for Author model
# Includes author's name and a nested list of all related books.
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer: show all books written by this author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # output includes author name + their books


"""
📖 Relationship Explanation:
- Each Author can have many Books (one-to-many).
- The AuthorSerializer uses the nested BookSerializer to automatically include
  details of all books related to that author.
- Example output:
  {
    "id": 1,
    "name": "George Orwell",
    "books": [
        {"id": 1, "title": "1984", "publication_year": 1949, "author": 1},
        {"id": 2, "title": "Animal Farm", "publication_year": 1945, "author": 1}
    ]
  }
"""
