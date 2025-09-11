# LibraryProject/bookshelf/models.py

from django.db import models

# You can leave it empty for now, or add a placeholder model:
class Placeholder(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
