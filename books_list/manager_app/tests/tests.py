import re
from _pytest.outcomes import importorskip
import pytest
from manager_app.tests.utils import fake_book_data
from manager_app.models import Book


@pytest.mark.django_db
def test_api_list_books(client, set_up):
    search_data = {"search": "a", "date_from": "1800-01-01", "date_to": "2021-01-07"}
    response2 = client.post("/books/api/", search_data, format="json")
    print(response2.content)
    assert response2.status_code == 200

    search_data = {
        "search": "a",
    }
    response2 = client.post("/books/api/", search_data, format="json")
    print(response2.content)
    assert response2.status_code == 200


@pytest.mark.django_db
def test_list_view(client, set_up):
    response = client.get('/books/list/', {})
    assert response.status_code == 200
    assert Book.objects.all().count() == len(response.context['books'])
    
    search_data = {
        'search': 'an',
        'date_from': '',
        'date_to': ''
    }
    response = client.post('/books/list/', search_data)
    assert response.status_code == 200
    assert Book.objects.all().count() != len(response.context['books'])
    assert response.context['books']

@pytest.mark.django_db
def test_add_book_view(client, set_up):
    books_count = Book.objects.all().count()
    create_data = fake_book_data()
    response = client.post('/books/add/', create_data)
    assert response.status_code == 302
    assert books_count == Book.objects.all().count() -1

@pytest.mark.django_db
def test_edit_book_view(client, set_up):
    books_count = Book.objects.all().count()
    book = Book.objects.all().first()
    book_title = book.title
    book_author = book.author
    book_date_of_publication = book.date_of_publication
    book_isbn = book.isbn
    book_pages = book.pages
    book_cover = book.cover
    book_lang = book.lang
    book_id = book.id
    edit_data = fake_book_data()
    
    response = client.post(f'/books/edit/{book_id}/', edit_data)
    
    assert response.status_code == 302
    assert books_count == Book.objects.all().count()
    book = Book.objects.get(id=book_id)
    assert book_title != book.title
    assert book.title
    assert book_author != book.author
    assert book.author
    assert book_date_of_publication != book.date_of_publication
    assert book.date_of_publication
    assert book_isbn != book.isbn
    assert book.isbn
    assert book_pages != book.pages
    assert book.pages
    assert book_cover != book.cover
    assert book.cover
    assert book_lang != book.lang
    assert book.lang
    
@pytest.mark.django_db
def test_import_view(client, set_up):
    response = client.get('/books/import/', {})
    assert response.status_code == 200
    try:
        session_data = response.context['answer']
    except KeyError:
        session_data = []
    import_data = {
        'title': 'ogniem',
        'author': 'sienkiewicz',
    }
    response = client.post('/books/import/', import_data)
    assert response.status_code == 302
    response = client.get('/books/import/', {})
    assert response.status_code == 200
    assert session_data != response.context['answer']
    assert 'niem' in response.context['answer'][0]['title']

@pytest.mark.django_db
def test_save_one_book_view(client, set_up):
    books_count = Book.objects.all().count()
    import_data = {
        'title': 'ogniem',
        'author': 'sienkiewicz',
    }
    response = client.post('/books/import/', import_data)
    assert response.status_code == 302
    response = client.get('/books/import/', {})
    chosen_book_lp = response.context['answer'][0]['lp']
    response = client.post('/books/save/', {'lp': str(chosen_book_lp)})
    assert response.status_code == 302
    assert books_count == Book.objects.all().count() - 1
    
    
@pytest.mark.django_db
def test_save_all_book_view(client, set_up):
    books_count = Book.objects.all().count()
    import_data = {
        'title': 'ogniem',
        'author': 'sienkiewicz',
    }
    response = client.post('/books/import/', import_data)
    assert response.status_code == 302
    response = client.get('/books/import/', {})
    # assert response.status_code == 200
    # imported_books = len(response.context['answer'])
    
    response = client.post('/books/save/all/', {})
    assert response.status_code == 302
    assert Book.objects.all().count() > books_count
    
    
