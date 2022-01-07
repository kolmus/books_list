from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=128, required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     search = cleaned_data.get("search")
    #     date_from = cleaned_data.get("date_from")
    #     date_to = cleaned_data.get("date_to")
    #     if not search and not date_from and not date_to:
    #         raise serializers.ValidationError("Minimum 1 field is required")
    #     return cleaned_data


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "date_of_publication", "isbn", "pages", "cover", "lang"]
