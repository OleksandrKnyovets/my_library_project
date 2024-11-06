from django.shortcuts import render, get_object_or_404, redirect  # Імпорт функцій для рендерингу, отримання об'єкта або редиректу
from .models import Book, Author, Review, User  # Імпорт моделей Book, Author, Review, User
from django.contrib.auth.decorators import login_required  # Імпорт декоратора для обмеження доступу неавторизованим користувачам
from django.contrib.auth import login, authenticate, logout  # Імпорт функцій для входу, автентифікації та виходу з облікового запису
from django.contrib.auth.forms import AuthenticationForm  # Імпорт форми аутентифікації користувача
from django.shortcuts import render, redirect  # Імпорт функцій рендерингу та редиректу
from .forms import UserRegisterForm, UserLoginForm  # Імпорт форм для реєстрації та входу
from django.contrib import messages  # Імпорт для роботи з повідомленнями

def book_list(request):
    books = Book.objects.all()  # Отримуємо всі книги
    query = request.GET.get('q')  # Отримуємо пошуковий запит
    sort_option = request.GET.get('sort', '')  # Отримуємо параметр сортування
    if query:
        books = books.filter(title__icontains=query)  # Фільтрація книг за назвою
    if sort_option == 'title_asc':
        books = books.order_by('title')  # Сортування за назвою по зростанню
    elif sort_option == 'title_desc':
        books = books.order_by('-title')  # Сортування за назвою по спаданню
    elif sort_option == 'author_asc':
        books = books.order_by('author__name')  # Сортування за іменем автора по зростанню
    elif sort_option == 'author_desc':
        books = books.order_by('-author__name')  # Сортування за іменем автора по спаданню
    return render(request, 'book_list.html', {'books': books})  # Відображення списку книг

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)  # Отримуємо книгу або повертаємо 404
    ratings = range(1, 6)  # Оцінки від 1 до 5
    reviews = book.reviews.all()  # Отримуємо всі відгуки книги
    return render(request, 'book_detail.html', {
        'book': book,
        'ratings': ratings,
        'reviews': reviews,  # Відгуки передаються в шаблон
    })

@login_required
def save_book(request, book_id):
    if request.method == "POST" and request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)  # Отримуємо книгу
        request.user.saved_books.add(book)  # Додаємо книгу до обраного
        return redirect('book_detail', book_id=book.id)  # Повертаємося до сторінки книги
    return redirect('login')  # Якщо не авторизований, перенаправляємо на вхід

@login_required
def user_favorites(request):
    return render(request, 'user_favorites.html', {'books': request.user.saved_books.all()})  # Відображаємо улюблені книги користувача

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)  # Форма реєстрації з даними
        if form.is_valid():
            user = form.save()  # Зберігаємо нового користувача
            login(request, user)  # Вхід нового користувача
            messages.success(request, "Ви успішно зареєструвалися!")  # Повідомлення про успіх
            return redirect('book_list')  # Переадресація до списку книг
        else:
            messages.error(request, "Помилка під час реєстрації.")  # Повідомлення про помилку
    else:
        form = UserRegisterForm()  # Порожня форма реєстрації
    return render(request, 'register.html', {'form': form})  # Відображаємо сторінку реєстрації

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # Форма входу з даними
        if form.is_valid():
            user = form.get_user()  # Отримуємо користувача
            login(request, user)  # Вхід користувача
            messages.success(request, "Ви успішно увійшли!")  # Повідомлення про успіх
            return redirect('book_list')  # Переадресація до списку книг
        else:
            messages.error(request, "Помилка на вході.")  # Повідомлення про помилку
    else:
        form = UserLoginForm()  # Порожня форма входу
    return render(request, 'login.html', {'form': form})  # Відображаємо сторінку входу

def user_logout(request):
    logout(request)  # Вихід з облікового запису
    messages.success(request, "Ви вийшли з облікового запису.")  # Повідомлення про успіх
    return redirect('book_list')  # Повертаємося до списку книг

def user_favorites(request):
    if request.user.is_authenticated:
        favorites = request.user.saved_books.all()  # Отримуємо улюблені книги користувача
        sort_option = request.GET.get('sort', '')  # Параметр сортування
        if sort_option == 'title_asc':
            favorites = favorites.order_by('title')  # Сортування за назвою по зростанню
        elif sort_option == 'title_desc':
            favorites = favorites.order_by('-title')  # Сортування за назвою по спаданню
        elif sort_option == 'author_asc':
            favorites = favorites.order_by('author__name')  # Сортування за іменем автора по зростанню
        elif sort_option == 'author_desc':
            favorites = favorites.order_by('-author__name')  # Сортування за іменем автора по спаданню
    else:
        favorites = []  # Порожній список, якщо користувач не авторизований
    return render(request, 'user_favorites.html', {'favorites': favorites})  # Відображаємо улюблені книги

def add_review(request, book_id):
    if request.method == "POST":
        book = get_object_or_404(Book, id=book_id)  # Отримуємо книгу або повертаємо 404
        rating = request.POST.get('rating')  # Отримуємо рейтинг
        comment = request.POST.get('comment')  # Отримуємо коментар
        Review.objects.update_or_create(
            book=book,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}  # Оновлюємо або створюємо відгук
        )
        return redirect('book_detail', book_id=book.id)  # Повернення на деталі книги
