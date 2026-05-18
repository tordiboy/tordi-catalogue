from django.contrib import admin
from .models import Book, UserBook, Category


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discounted_price')

admin.site.register(UserBook)
admin.site.register(Category)