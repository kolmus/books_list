from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

import requests
from requests.sessions import Request

from .models import Book
from .forms import GoogleApiForm

# Create your views here.
class BooksListView(View):
    def get(self, request):
        """View to list all books 

        Returns:
            books [queryset]: all books in DB
        """        
        books = Book.objects.all().order_by('id')
        return render(request, 'manager_app/books_list.html', {'books': books})
    
    def post(self, request):
        """Viev to filter bay title, author, language or date of publiation

        Returns:
            books: queryset of all books if exeptions or empty fields
            books: list with object => result of filtering
            
        """        
        search = request.POST['search']
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']
        books = Book.objects.all().order_by('id')
        result_search = []

        if search:       # filter by title, author and language
            for book in books:
                if book in books.filter(title__icontains=search):
                    result_search.append(book)
                if book in books.filter(author__icontains=search):
                    result_search.append(book)
                if book in books.filter(lang__icontains=search):
                    result_search.append(book)

        result_date = []
        if date_from and date_to:       # filter by date
            books_pub_to = books.filter(date_of_publication__lte=date_to)
            for book in books_pub_to.filter(date_of_publication__gte=date_from):
                result_date.append(book)
        elif date_from:
            for book in books.filter(date_of_publication__gte=date_from):
                result_date.append(book)
        elif date_to:
            for book in books.filter(date_of_publication__lte=date_to):
                result_date.append(book)
        
        if result_search:
            if result_date:
                result = []                 #if search and date check for both results 
                for i in result_date:
                    if i in result_search:
                        result.append(i)
            else:
                result = result_search         # if no date and search
        elif result_date:                      # if no search and date
            result = result_date
        else:                                  # if no date and no search
            result = books
        return render(request, 'manager_app/books_list.html', {"books": result})


class BookCreateView(CreateView):
    """Generic view to create new book

    """
    model = Book
    fields = '__all__'
    success_url = '/books/list/'


class BookUpdateView(UpdateView):
    """Generic view to update book

    Args:
        pk (int): id of book
    """    
    model = Book
    fields = '__all__'
    success_url = '/books/list/'


class BookImportView(View):
    def get(self, request):
        form = GoogleApiForm()
        return render(request, 'manager_app/books_import.html', {'form': form})
    
    def post(self, request):
        from books_list.local_settings import GOOGLE_API_KEY
        form = GoogleApiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            title_new = title.replace(" ", "+")
            author_new = author.replace(" ", "+")
            response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title_new}+inauthor:{author_new}&key={GOOGLE_API_KEY}')
            response.raise_for_status()
            if response.status_code == 200:
                answer = response.json()['items'][0][title]
            else: 
                answer = 'not working'
            return render(request, 'manager_app/books_import.html', {'form': form, "answer": answer} )


"""
200 OK

{
    "kind": "books#volumes",
    "items": [
        {
            "kind": "books#volume",
            "id": "_ojXNuzgHRcC",
            "etag": "OTD2tB19qn4",
            "selfLink": "https://www.googleapis.com/books/v1/volumes/_ojXNuzgHRcC",
            "volumeInfo": {
            "title": "Flowers",
            "authors": [
                "Vijaya Khisty Bodach"
            ],
        ...
        },
        {
        "kind": "books#volume",
        "id": "RJxWIQOvoZUC",
        "etag": "NsxMT6kCCVs",
        "selfLink": "https://www.googleapis.com/books/v1/volumes/RJxWIQOvoZUC",
        "volumeInfo": {
            "title": "Flowers",
            "authors": [
                "Gail Saunders-Smith"
            ],
            ...
        },
        {
        "kind": "books#volume",
        "id": "zaRoX10_UsMC",
        "etag": "pm1sLMgKfMA",
        "selfLink": "https://www.googleapis.com/books/v1/volumes/zaRoX10_UsMC",
        "volumeInfo": {
            "title": "Flowers",
            "authors": [
                "Paul McEvoy"
            ],
            ...
        },
        "totalItems": 3
}
"""