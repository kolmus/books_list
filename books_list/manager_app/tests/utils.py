from faker import Faker
from random import randint

from manager_app.models import Book

faker = Faker("pl_PL")


def fake_book_data():
    """Generate fake data for Book

    Returns:
        dictionary
    """
    return {
        "title": f"{faker.job()} {faker.name()}",
        "author": f"{faker.first_name()} {faker.last_name()}",
        "date_of_publication": f"{faker.date()}",
        "isbn": f"{faker.isbn13()}",
        "pages": randint(60, 1300),
        "cover": f"{faker.image_url()}",
        "lang": f"{faker.language_code()}",
    }


def create_fake_book():
    """
    Create fake Book
    """
    Book.objects.create(**fake_book_data())
