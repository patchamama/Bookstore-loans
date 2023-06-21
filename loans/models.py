from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Returned"), (1, "Loaned"))


class Books(models.Model):
    title = models.CharField(max_length=150, unique=False)
    author = models.CharField(max_length=150, unique=False)
    number_of_items = models.IntegerField(default=1)
    items_to_loan = models.IntegerField(default=0)
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
        return f"{self.author} - {self.title} ({self.number_of_items} books, {self.items_to_loan} to loans)"

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
    number_renowals = models.IntegerField(default=1)
    status = models.IntegerField(choices=STATUS, default=1)
    returned_on = models.DateTimeField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Loan {self.book} by {self.user}. Expire {self.expire}, renowals (self.number_renowals)"
