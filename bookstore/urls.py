from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('loans.urls'), name='loans_urls'),
    path('accounts/', include('allauth.urls')),
]
