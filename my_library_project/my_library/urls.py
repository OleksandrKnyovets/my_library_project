from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),                            # Головна сторінка зі списком книг
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),     # Детальна інформація про книгу
    path('book/<int:book_id>/save/', views.save_book, name='save_book'),    # Збереження книги до обраного
    path('favorites/', views.user_favorites, name='user_favorites'),        # Сторінка з улюбленими книгами користувача
    path('register/', views.register, name='register'),                     # Сторінка реєстрації
    path('login/', views.user_login, name='login'),                         # Сторінка входу
    path('logout/', views.user_logout, name='logout'),                      # Вихід з облікового запису
    path('save_book/<int:book_id>/', views.save_book, name='save_book'),    # Збереження книги до обраного (дубль)
    path('book/<int:book_id>/add_review/', views.add_review, name='add_review'),  # Додавання відгуку для книги
]
