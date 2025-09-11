from django.contrib import admin
from .models import Book

# Basic registration
# admin.site.register(Book)

# Customized admin configuration
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ( 'author',)
    search_fields = ('title', 'author')