from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Book, Loan
from .forms import CommentForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


class BookList(generic.ListView):
    model = Book
    queryset = Book.objects.order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        if ('q' in request.POST):
            search = request.POST['q']
            qsearch = Q(Q(title__icontains=search) | Q(author__icontains=search) | Q(features__icontains=search))
            booklist = Book.objects.filter(qsearch).order_by('-created_on')
        else:
            booklist = Book.objects.all()

        return render(
        request,
        "index.html",
        {
            "book_list": booklist,
        },
        )


class BookDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Book.objects
        book = get_object_or_404(queryset, slug=slug)
        comments = book.book_comments.filter(approved=True).order_by("-created_on")
        loans = book.book_loans.filter(user=request.user, status__lt=3).order_by("-created_on")
        message_action = ""
        
        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "comments": comments,
                "loans": loans,
                "commented": False,
                "comment_form": CommentForm(),
                "message_action": message_action
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Book.objects
        book = get_object_or_404(queryset, slug=slug)
        comments = book.book_comments.filter(approved=True).order_by("-created_on")
        loans = book.book_loans.filter(user=request.user, status__lt=3).order_by("-created_on")

        message_action = ""
        is_commented = False
        
        if ('action' in request.POST):
            if (request.POST['action'] == "add_reserved"):
                loandata = Loan.objects.create(
                    expire = timezone.now() + timedelta(days=7), 
                    number_renowals = 0,
                    status = 1,
                    book=book, 
                    user=request.user)
                loandata.save()
                loans = book.book_loans.filter(user=request.user, status__lt=3).order_by("-created_on")
                message_action = "Reserve added!"


            if (request.POST['action'] == "remove_reserved"):
                if Loan.objects.filter(user=request.user, book=book, status=1).exists():
                    Loan.objects.filter(user=request.user, book=book, status=1).delete()
                    #loandata = Loan.objects.get(user=request.user, book=book, status=1)
                    #loandata.number_renowals = 0
                    #loandata.expire = timezone.now()
                    #loandata.status = 4 ## 1 Reserved to (4, "Canceled")
                    #loandata.save()
                    loans = book.book_loans.filter(user=request.user, status__lt=3).order_by("-created_on")
                    message_action = "Reserve removed!"
        else:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                comment_form.instance.email = request.user.email
                comment_form.instance.name = request.user.username
                comment = comment_form.save(commit=False)
                comment.book = book
                comment.save()
                is_commented = True
            else:
                comment_form = CommentForm()
            
        return render(
            request,
            "book_detail.html",
            {
                "book": book,
                "comments": comments,
                "loans": loans,
                "commented": is_commented,
                "comment_form": CommentForm(),
                "message_action": message_action
            },
        ) 


class LoanDetail(generic.ListView):
    

    def get(self, request, *args, **kwargs):
        queryset = Loan.objects
        loans = Loan.objects.filter(
            user=self.request.user
        ).order_by('-expire', 'status')
        message_action = ""

        return render(
            request,
            "loans_detail.html",
            {
                "myloans": loans,
                "message_action": message_action
            },
        )

    def post(self, request, *args, **kwargs):
        queryset = Loan.objects
        loans = Loan.objects.filter(
            user=self.request.user
        ).order_by('-expire', 'status')
        message_action = ""

        if (request.POST['action'] == "remove_reserved"):
            record_id = request.POST['id']
            #loandata = get_object_or_404(Loan, id=record_id)
            if Loan.objects.filter(id=record_id).exists():
                Loan.objects.filter(id=record_id).delete()
                message_action = "Reserve removed!"
                #loandata = Loan.objects.get(id=record_id)
                #loandata.number_renowals = 0
                #loandata.expire = timezone.now()
                #loandata.status = 4 ## 1 Reserved to (4, "Canceled")
                #loandata.save()
        if ('action' in request.POST):
            if (request.POST['action'] == "add_renowals"):
                record_id = request.POST['id']
                if Loan.objects.filter(id=record_id).exists():
                    #Loan.objects.filter(id=record_id).delete()
                    loandata = Loan.objects.get(id=record_id)
                    loandata.expire = loandata.expire + timedelta(days=30)
                    loandata.number_renowals = loandata.number_renowals + 1
                    loandata.save()
                    message_action = "Renowals added!"

            if (request.POST['action'] == "add_reserved"):
                record_id = request.POST['id']
                if Loan.objects.filter(id=record_id).exists():
                    #Loan.objects.filter(id=record_id).delete()
                    loandata = Loan.objects.get(id=record_id)
                    loandata.expire = timezone.now() + timedelta(days=7)
                    loandata.number_renowals = 0
                    loandata.status = 1 ## (4, "Canceled") to 1 Reserved 
                    loandata.save()
                    message_action = "Reserve added!"

        return render(
            request,
            "loans_detail.html",
            {
                "myloans": loans,
                "message_action": message_action
            },
        ) 



