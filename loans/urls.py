from . import views
from django.urls import path

urlpatterns = [
    path('', views.BookList.as_view(), name='home'),
    path('loans/', views.LoanDetail.as_view(), name='loan_detail'),
    path('<slug:slug>/', views.BookDetail.as_view(), name='book_detail'),
]


