from . import views
from django.urls import path
from django.conf.urls import handler400, handler403, handler404, handler500
from loans.views import Error400View, Error403View, Error404View, Error500View

urlpatterns = [
    path('', views.BookList.as_view(), name='home'),
    path('loans/', views.LoanDetail.as_view(), name='loan_detail'),
    path('<slug:slug>/', views.BookDetail.as_view(), name='book_detail'),
]

handler400 = Error400View.as_view()
handler403 = Error403View.as_view()
handler404 = Error404View.as_view()
handler500 = Error500View.as_error_view()