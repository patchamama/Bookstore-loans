from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Book


class BookList(generic.ListView):
    model = Book
    queryset = Book.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 12


class BookDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Book.objects
        book = get_object_or_404(queryset, slug=slug)
        comments = book.book_comments.filter(approved=True).order_by("-created_on")

        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "comments": comments
            },
        )