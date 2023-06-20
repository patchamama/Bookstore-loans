from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Books(models.Model):
    title = models.CharField(max_length=150, unique=False)
    author = models.CharField(max_length=150, unique=False)
    copies = models.IntegerField(default=1)
    can_loan = models.BooleanField(default=False)
    pub_year = models.DateTimeField()
    publisher = models.CharField(max_length=100, unique=False)
    pages = models.IntegerField(default=0)
    isbn = models.CharField(max_length=13, unique=True)
    translators = models.CharField(max_length=200, unique=False)
    description = models.TextField(blank=True)
    cover = CloudinaryField('image', default='placeholder')
    features = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_loans(self):
        return self.loans.count()


def add_one_month_at_today():
    return timezone.now() + timedelta(days=30)


class Loans(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE,
                             related_name="loans")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="loans")
    expire = models.DateTimeField(default=add_one_month_at_today, blank=True)
    renewals = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
