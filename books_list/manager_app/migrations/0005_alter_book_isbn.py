# Generated by Django 4.0.1 on 2022-01-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager_app", "0004_alter_book_date_of_publication"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(max_length=32, verbose_name="ISBN"),
        ),
    ]
