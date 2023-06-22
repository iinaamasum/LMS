from .models import BorrowedBook
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Book
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'library/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        # Implement user authentication logic here
        return redirect('home')
    return render(request, 'library/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def book_catalog(request):
    books = Book.objects.all()
    return render(request, 'library/book_catalog.html', {'books': books})


def book_search(request):
    query = request.GET.get('query')
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'library/book_search.html', {'books': books})


@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.availability:
        due_date = timezone.now() + timedelta(days=7)
        borrowed_book = BorrowedBook(
            user=request.user, book=book, due_date=due_date)
        borrowed_book.save()
        book.availability = False
        book.save()
        return redirect('book_catalog')
    else:
        # Handle book not available scenario
        pass


@login_required
def return_book(request, book_id):
    borrowed_book = BorrowedBook.objects.get(
        book_id=book_id, user=request.user)
    borrowed_book.returned = True
    borrowed_book.save()
    book = borrowed_book.book
    book.availability = True
    book.save()
    return redirect('book_catalog')


@login_required
def add_to_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)
    return redirect('book_catalog')


@login_required
def remove_from_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.books.remove(book)
    return redirect('book_catalog')
