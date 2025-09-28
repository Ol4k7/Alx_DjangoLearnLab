from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books / Create a new book
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: anyone can view, only authenticated users can create
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # Step 3: Customize creation
    def perform_create(self, serializer):
        # Example: you could attach the logged-in user
        # serializer.save(owner=self.request.user)
        serializer.save()


# Retrieve a single book / Update / Delete
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: only authenticated users can update/delete
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    # Step 3: Customize update
    def perform_update(self, serializer):
        # Example: log or enforce extra validation before saving
        serializer.save()
