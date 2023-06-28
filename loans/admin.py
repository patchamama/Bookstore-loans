from django.contrib import admin
from .models import Book, Comment, Loan
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.auth import get_user_model


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    """Allows admin to manage Book via the admin panel"""
    list_display = ("title", "author", "items_to_loan", "created_on")
    search_fields = ["title", "author", "description", "features"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("created_on", "publisher")
    summernote_field = "description"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Allows admin to manage Comment via the admin panel"""
    list_display = ("name", "comment", "book", "created_on", "approved")
    search_fields = ["name", "email", "comment"]
    list_filter = ("created_on", "approved")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Allows admin to manage Loan via the admin panel"""
    def get_changeform_initial_data(self, request):
        get_data = super(LoanAdmin, self).get_changeform_initial_data(request)
        get_data["user"] = request.user.pk
        return get_data

    list_display = ("book", "user", "expire", "number_renowals", "status")
    search_fields = ["book", "user"]
    list_filter = ("user",)
