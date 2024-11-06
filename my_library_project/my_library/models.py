from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель користувача
class User(AbstractUser):
    # Поле для збереження улюблених книг (Many-to-Many зв’язок із моделлю Book)
    saved_books = models.ManyToManyField(
        'Book',  # Зв'язок з моделлю Book
        related_name='saved_by',  # Ім'я для доступу до зворотного зв’язку (книги, збережені користувачами)
        blank=True  # Поле може бути пустим
    )

    # Додаткове поле для фотографії профілю
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Додаткове поле для біографії
    bio = models.TextField(blank=True, null=True)

    # Метод __str__ для відображення імені користувача
    def __str__(self):
        return self.username


# Модель автора
class Author(models.Model):
    # Поле для імені автора
    name = models.CharField(max_length=255)
    
    # Поле для біографії автора
    biography = models.TextField()

    # Метод __str__ для відображення імені автора
    def __str__(self):
        return self.name


# Модель книги
class Book(models.Model):
    # Назва книги
    title = models.CharField(max_length=255)
    
    # Опис книги
    description = models.TextField()
    
    # Дата публікації книги
    publication_date = models.DateField()
    
    # Зв'язок з автором (ForeignKey), зв’язуємо кожну книгу з конкретним автором
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    # Поле для файлу книги, який можна завантажити (наприклад, PDF)
    file = models.FileField(upload_to='.')

    # Метод __str__ для відображення назви книги
    def __str__(self):
        return self.title


# Модель відгуків для книг
class Review(models.Model):
    # Зв'язок з книгою, до якої стосується відгук
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    
    # Зв'язок з користувачем, який залишив відгук
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    
    # Рейтинг книги від 1 до 5
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    
    # Коментар користувача (може бути пустим)
    comment = models.TextField(blank=True, null=True)

    # Встановлення унікальності - один користувач може залишити один відгук на одну книгу
    class Meta:
        unique_together = ('book', 'user')

    # Метод __str__ для відображення інформації про відгук
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating})"
