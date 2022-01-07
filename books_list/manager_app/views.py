from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

from .models import Book
from .forms import GoogleApiForm
from .serializers import BookListSerializer, BookSerializer


def book_search(books, search="", date_from="", date_to=""):
    """Function help to filter database with several args
    Checking if str icontains in title, author or language,

    Checking if publication date is betweerg arguments
    Args:
        search (str): for fields filtering.
        date_from (str): date in format "YYYY-MM-DD"
        date_to (str): date in format "YYYY-MM-DD"
        books (queryset): checked set of data

    Returns:
        [queryset]: objects of Book model
    """
    result_search = []

    if search:  # filter by title, author and language
        for book in books:
            if book in books.filter(title__icontains=search):
                result_search.append(book.id)
            if book in books.filter(author__icontains=search):
                result_search.append(book.id)
            if book in books.filter(lang__icontains=search):
                result_search.append(book.id)

    result_date = []
    if date_from and date_to:  # filter by date
        books_pub_to = books.filter(date_of_publication__lte=date_to)
        for book in books_pub_to.filter(date_of_publication__gte=date_from):
            result_date.append(book.id)
    elif date_from:
        for book in books.filter(date_of_publication__gte=date_from):
            result_date.append(book.id)
    elif date_to:
        for book in books.filter(date_of_publication__lte=date_to):
            result_date.append(book.id)

    if result_search:
        if result_date:
            result_ids = []  # if search and date check for both results
            for i in result_date:
                if i in result_search:
                    result_ids.append(i)
        else:
            result_ids = result_search  # if no date and search
    elif result_date:  # if no search and date
        result_ids = result_date
    else:  # if no date and no search
        result_ids = []
    result = books.filter(id__in=result_ids)
    return result


class BooksListView(View):
    def get(self, request):
        """View to list all books

        Returns:
            books [queryset]: all books in DB
        """
        books = Book.objects.all().order_by("id")

        if books.exists():
            return render(request, "manager_app/books_list.html", {"books": books})
        else:
            return render(request, "manager_app/books_list.html")

    def post(self, request):
        """View to filter by title, author, language or date of publication

        Returns:
            books: Queryset => result of filtering
        """
        search = request.POST["search"]
        date_from = request.POST["date_from"]
        date_to = request.POST["date_to"]
        books = Book.objects.all().order_by("id")
        if books.exists():
            result = book_search(search, date_from, date_to, books)
            # books = Book.objects.filter(title__icontains=search, )
            return render(request, "manager_app/books_list.html", {"books": result})
        else:  # response = client.get("/books/api/a/1900-01-01/2021-01-07/", {}, format='json')
            # print(response.content)
            # assert response.status_code == 200
            return render(request, "manager_app/books_list.html")


class BookCreateView(CreateView):
    """Generic view to create new book"""

    model = Book
    fields = "__all__"
    success_url = "/books/list/"


class BookUpdateView(UpdateView):
    """Generic view to update book

    Args:
        pk (int): id of book
    """

    model = Book
    fields = "__all__"
    success_url = "/books/list/"


class BookImportView(View):
    def get(self, request):
        """listing las imported books and alows to import other books

        Returns:
            form: needed to create request
            answer: list of books(dictionaries) with last response
        """
        form = GoogleApiForm()
        try:
            answer = request.session["imported_books"]
            return render(request, "manager_app/books_import.html", {"form": form, "answer": answer})
        except KeyError:
            return render(request, "manager_app/books_import.html", {"form": form})

    def post(self, request):
        """Makes fetch to Googele Books API,
        saves needed data in users cache in session,
        redirects (GET)to import page

        """
        from books_list.local_settings import GOOGLE_API_KEY

        form = GoogleApiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            title_new = title.replace(" ", "+")
            author_new = author.replace(" ", "+")
            response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={title_new}+inauthor:{author_new}&key={GOOGLE_API_KEY}")
            response.raise_for_status()

            if response.status_code == 200:
                answer = response.json()["items"]

                list_of_books = []
                for i in range(len(answer)):
                    print(i)
                    print(answer[i]["volumeInfo"])
                    book = {}
                    book["lp"] = i
                    book["title"] = answer[i]["volumeInfo"]["title"]
                    book["author"] = ", ".join(answer[i]["volumeInfo"]["authors"])
                    try:
                        date_publ = answer[i]["volumeInfo"]["publishedDate"]
                        if len(date_publ) == 4:
                            book["date_of_publication"] = date_publ + "-01-01"
                        else:
                            book["date_of_publication"] = date_publ
                    except KeyError:
                        pass
                    print(answer[i]["volumeInfo"]["industryIdentifiers"][0]["identifier"])
                    book["isbn"] = answer[i]["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                    try:
                        book["pages"] = answer[i]["volumeInfo"]["pageCount"]
                    except KeyError:
                        pass
                    try:
                        book["cover"] = answer[i]["volumeInfo"]["imageLinks"]["thumbnail"]
                    except KeyError:
                        pass
                    book["lang"] = answer[i]["volumeInfo"]["language"]
                    list_of_books.append(book)
            request.session["imported_books"] = list_of_books
            # to write exeptions
            return redirect("/books/import/")


class BookSaveView(View):
    """
    Saves new 1 Book from cache data
    """

    def post(self, request):
        lp = request.POST["lp"]

        try:
            books = request.session["imported_books"]
        except KeyError:
            return redirect("/books/import/")

        new_books = []
        for i in range(len(books)):
            book = books[i]
            if book["lp"] == int(lp):
                print(book)
                new_book = Book()
                new_book.title = book["title"]
                new_book.author = book["author"]
                new_book.isbn = book["isbn"]
                try:
                    new_book.pages = int(book["pages"])
                except KeyError:
                    pass
                try:
                    new_book.cover = book["cover"]
                except KeyError:
                    pass
                new_book.lang = book["lang"]
                new_book.save()
                try:
                    new_book.date_of_publication = book["date_of_publication"]
                    new_book.save()
                except KeyError:
                    pass
                except ValidationError:
                    pass
                continue
            new_books.append(books[i])
        request.session["imported_books"] = new_books
        # @lru_cache to check


class BookSaveAll(View):
    """
    saves all improrted books in database
    """

    def post(self, request):
        try:
            books = request.session["imported_books"]
        except KeyError:
            return redirect("/books/import/")
        for book in books:
            new_book = Book()
            new_book.title = book["title"]
            new_book.author = book["author"]
            new_book.isbn = book["isbn"]
            new_book.lang = book["lang"]
            new_book.save()

            try:
                new_book.pages = int(book["pages"])
            except KeyError:
                pass
            try:
                new_book.cover = book["cover"]
            except KeyError:
                pass
            try:
                new_book.date_of_publication = book["date_of_publication"]
                new_book.save()
            except KeyError:
                pass
            except ValidationError:
                pass
        try:
            del request.session["imported_books"]
        except KeyError:
            pass
        return redirect("/books/import/")


class BookSearchApiView(APIView):
    """APIView to filter by title, author, language or date of publication

    Returns:
        result: queryset => result of filtering
    """

    def post(self, request, format=None):
        books = Book.objects.all()
        serializer = BookListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                search = serializer.data["search"]
            except KeyError:
                search = ""
            try:
                date_from = serializer.data["date_from"]
            except KeyError:
                date_from = ""
            try:
                date_to = serializer.data["date_to"]
            except KeyError:
                date_to = ""

            result = book_search(search=search, date_to=date_to, date_from=date_from, books=books)

        if result.exists():
            data = {"books": BookSerializer(result, many=True).data}
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise Http404
