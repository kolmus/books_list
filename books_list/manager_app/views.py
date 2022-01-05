from django.shortcuts import render
from django.views import View

from .models import Book

# Create your views here.
class BooksListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'books_list/list.html')
