from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Book, Loan
from .forms import CommentForm
from django.utils import timezone
from datetime import timedelta


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
        loans = book.book_loans.filter(user=request.user, status__lt=3).order_by("-created_on")

        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "comments": comments,
                "loans": loans,
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

class LoanDetail(generic.ListView):
    
    model = Loan
    #queryset = Loan.objects.filter(user=self.request.user).order_by('-created_on')
    template_name = 'loans_detail.html'
    context_object_name = 'myloans'

    def get_queryset(self):
        return Loan.objects.filter(
            user=self.request.user
        ).order_by('-expire', 'status')

    def post(self, request, *args, **kwargs):
        queryset = Loan.objects
        loans = Loan.objects.filter(
            user=self.request.user
        ).order_by('-expire', 'status')

        print(request.POST)
        if (request.POST['action'] == "remove_reserved"):
            record_id = request.POST['id']
            #loandata = get_object_or_404(Loan, id=record_id)
            if Loan.objects.filter(id=record_id).exists():
                #Loan.objects.filter(id=record_id).delete()
                loandata = Loan.objects.get(id=record_id)
                loandata.status = 4 ## Reserved to (4, "Canceled")
                loandata.save()

        if (request.POST['action'] == "add_renowals"):
            record_id = request.POST['id']
            if Loan.objects.filter(id=record_id).exists():
                #Loan.objects.filter(id=record_id).delete()
                loandata = Loan.objects.get(id=record_id)
                loandata.expire = loandata.expire + timedelta(days=30)
                loandata.number_renowals = loandata.number_renowals + 1
                loandata.save()

        return render(
            request,
            "loans_detail.html",
            {
                "myloans": loans
            },
        ) 



