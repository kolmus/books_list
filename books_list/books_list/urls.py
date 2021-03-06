"""books_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from manager_app.views import BookSearchApiView, BookSaveAll, BookSaveView, BooksListView, BookUpdateView, BookCreateView, BookImportView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/list/", BooksListView.as_view()),
    path("books/edit/<int:pk>/", BookUpdateView.as_view()),
    path("books/add/", BookCreateView.as_view()),
    path("books/import/", BookImportView.as_view()),
    path("books/save/", BookSaveView.as_view()),
    path("books/save/all/", BookSaveAll.as_view()),
    path("books/api/", BookSearchApiView.as_view()),
]
