from django.shortcuts import render
from django.views import generic
from .models import Book

class BookList(generic.ListView):
    model = Book
    queryset = Book.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 12
