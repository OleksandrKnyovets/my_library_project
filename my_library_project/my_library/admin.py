from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Author, Book, Review

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Отображение дополнительных полей в админке
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('saved_books', 'profile_picture', 'bio')}),
    )
    list_display = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author__name')
    list_filter = ('publication_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating')
    list_filter = ('rating',)