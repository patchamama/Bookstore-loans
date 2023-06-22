from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Book
from .forms import CommentForm


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
                "comments": comments,
                "commented": False,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Book.objects
        book = get_object_or_404(queryset, slug=slug)
        comments = book.book_comments.filter(approved=True).order_by("-created_on")

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.book = book
            comment.save()
        else:
            comment_form = CommentForm()


        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "comments": comments,
                "commented": True,
                "comment_form": CommentForm()
            },
        ) 
