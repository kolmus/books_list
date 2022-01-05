from django.shortcuts import render
from django.views import View

from .models import Book

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
        


