from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
from datetime import timedelta

STATUS = ((0, "Returned"), (1, "Loaned"))


class Book(models.Model):
    title = models.CharField(max_length=150, unique=False)
    slug = models.SlugField(max_length=155, unique=True)
    author = models.CharField(max_length=150, unique=False)
    number_of_items = models.IntegerField(default=1)
    items_to_loan = models.IntegerField(default=0)
    pub_year = models.DateTimeField(blank=True, null=True)
    publisher = models.CharField(max_length=100, unique=False, blank=True)
    pages = models.IntegerField(default=0)
    isbn = models.CharField(max_length=13, unique=False, blank=True)
    language = models.CharField(max_length=3, default="eng", unique=False)
    translators = models.CharField(max_length=200, unique=False, blank=True)
    description = models.TextField(blank=True)
    cover = CloudinaryField('image', default='notimage')
    features = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.author} - {self.title} ({self.number_of_items} books, {self.items_to_loan} to loans)"

    def items_available_to_loan(self):
        books_on_loan = self.items_to_loan - self.book_loans.count()
        if (books_on_loan > 0):
            return f" {books_on_loan} (of {self.items_to_loan})"
        else:
            return "0"



def add_one_month_at_today():
    return timezone.now() + timedelta(days=30)

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name="book_comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.comment} by {self.name}"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name="book_loans")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user_loans")
    expire = models.DateTimeField(default=add_one_month_at_today, blank=True)
    number_renowals = models.IntegerField(default=1)
    status = models.IntegerField(choices=STATUS, default=1, blank=True)
    returned_on = models.DateTimeField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Loan {self.book} by {self.user}. Expire {self.expire}, renowals (self.number_renowals)"

