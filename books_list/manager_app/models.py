from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=256, verbose_name='Tytuł')
    author = models.CharField(max_length=256, verbose_name='Autor')
    date_of_publication = models.DateField(verbose_name='Data publikacji')
    isbn = models.BigIntegerField(verbose_name='ISBN')
    pages = models.IntegerField(verbose_name='Liczba stron')
    cover = models.ImageField(upload_to='covers/', verbose_name='Okładka', null=True)
    lang = models.CharField(max_length=32, verbose_name='Język publikacji')
    
    def __str__(self):
        return f'{self.title} - {self.author} ({self.date_of_puclication})'
