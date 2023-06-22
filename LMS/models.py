from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    publication_date = models.DateField()
    genre = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)
    no_of_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
