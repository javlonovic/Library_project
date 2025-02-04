from django.contrib import admin
from .models import Book, Message

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'author')
    list_filter = ('published_date',)
    fields = ('title', 'author', 'description', 'published_date', 'cover_image', 'pdf_file')

admin.site.register(Book, BookAdmin)
admin.site.register(Message)