# Generated by Django 4.0.1 on 2022-01-06 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager_app', '0005_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.CharField(max_length=256, null=True, verbose_name='Okładka'),
        ),
    ]
