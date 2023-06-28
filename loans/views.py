from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Book, Loan, Comment
from .forms import CommentForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class BookList(generic.ListView):
    """
    The view is used to display book covers and some content on the home page
    """
    model = Book
    queryset = Book.objects.order_by("-created_on")
    template_name = "index.html"
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        """
        Function that filters the search in the navbar
        """
        if "q" in request.POST:
            search = request.POST["q"]
            qsearch = Q(
                Q(title__icontains=search)
                | Q(author__icontains=search)
                | Q(features__icontains=search)
            )
            booklist = Book.objects.filter(qsearch).order_by("-created_on")
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
    """
    The view displays details of a selected book and allows 
    you to reserve books for loan or comment on books.
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Function that returns the selected book and action messages.
        """
        queryset = Book.objects
        book = get_object_or_404(queryset, slug=slug)
        comments = book.book_comments.filter(approved=True).order_by("-created_on")
        if (request.user.is_authenticated):
            loans = book.book_loans.filter(user=request.user, status__lt=3).order_by(
            "-created_on")
        else:
            loans = []

        #Message to show in the template of one action
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
                "message_action": message_action,
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Function that saves changes requested 
        in the view: reserve a book, delete a 
        reservation, delete a comment
        """
        queryset = Book.objects
        book = get_object_or_404(queryset, slug=slug)
        comments = book.book_comments.filter(approved=True).order_by(
            "-created_on")
        loans = book.book_loans.filter(user=request.user, status__lt=3).order_by(
            "-created_on"
        )

        #Message to show in the template of one action
        message_action = ""
        is_commented = False

        
        if "action" in request.POST:
            # Reserve a book
            if request.POST["action"] == "add_reserved":
                loandata = Loan.objects.create(
                    expire=timezone.now() + timedelta(days=7),
                    number_renowals=0,
                    status=1,
                    book=book,
                    user=request.user,
                )
                loandata.save()
                loans = book.book_loans.filter(
                    user=request.user, status__lt=3
                ).order_by("-created_on")
                message_action = "Reserve added!"

            # Delete a reservation
            if request.POST["action"] == "remove_reserved":
                if Loan.objects.filter(user=request.user, book=book, status=1).exists():
                    Loan.objects.filter(user=request.user, book=book, status=1).delete()
                    loans = book.book_loans.filter(
                        user=request.user, status__lt=3
                    ).order_by("-created_on")
                    message_action = "Reserve removed!"

            #Delete a comment
            if request.POST["action"] == "delete_comment":
                comment_id = request.POST["id"]
                if Comment.objects.filter(name=request.user, id=comment_id).exists():
                    Comment.objects.filter(name=request.user, id=comment_id).delete()
                    comments = Comment.objects.filter(book=book).order_by(
                        "-created_on")
                    message_action = "Comment deleted!"

        else:
            # Form comment submit (not action in post)
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
                "message_action": message_action,
            },
        )



class LoanDetail(LoginRequiredMixin, generic.ListView):
    """
    View that allows you to visualize loans, their status 
    and perform actions: cancel reservation, extend loan...
    """

    def get(self, request, *args, **kwargs):
        """
        Function that returns all the loans of the active user.
        """
        queryset = Loan.objects            
        loans = Loan.objects.filter(user=self.request.user).order_by(
            "-expire", "status"
            )

        #Action to show in template
        message_action = ""

        return render(
            request,
            "loans_detail.html",
            {"myloans": loans, "message_action": message_action},
        )

    def post(self, request, *args, **kwargs):
        """
        Function that allows you to change the status of a loan
        """
        queryset = Loan.objects
        loans = Loan.objects.filter(user=self.request.user).order_by(
            "-expire", "status"
        )
        message_action = ""

        # Process different actions en view
        if "action" in request.POST:

            #Remove reserved (loan deleted)
            if request.POST["action"] == "remove_reserved":
                record_id = request.POST["id"]
                if Loan.objects.filter(id=record_id).exists():
                    Loan.objects.filter(id=record_id).delete()
                    message_action = "Reserve removed!"

            #+Loan extension
            if request.POST["action"] == "add_renowals":
                record_id = request.POST["id"]
                if Loan.objects.filter(id=record_id).exists():
                    loandata = Loan.objects.get(id=record_id)
                    loandata.expire = loandata.expire + timedelta(days=30)
                    loandata.number_renowals = loandata.number_renowals + 1
                    loandata.save()
                    message_action = "Renowals added!"

            #Add reservation of Loan
            if request.POST["action"] == "add_reserved":
                record_id = request.POST["id"]
                if Loan.objects.filter(id=record_id).exists():
                    loandata = Loan.objects.get(id=record_id)
                    loandata.expire = timezone.now() + timedelta(days=7)
                    loandata.number_renowals = 0
                    loandata.status = 1
                    loandata.save()
                    message_action = "Reserve added!"

        return render(
            request,
            "loans_detail.html",
            {"myloans": loans, "message_action": message_action},
        )



class Error400View(TemplateView):
    """Error 400 template to be show"""
    template_name = "templates/400.html"


class Error403View(TemplateView):
    """Error 403 template to be show"""
    template_name = "templates/403.html"


class Error404View(TemplateView):
    """Error 404 template to be show"""
    template_name = "templates/404.html"


class Error500View(TemplateView):
    """Error 500 template to be show"""
    template_name = "templates/500.html"

    @classmethod
    def as_error_view(cls):
        v = cls.as_view()

        def view(request):
            r = v(request)
            r.render()
            return r

        return view
