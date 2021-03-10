from django.db import transaction
from rest_framework import serializers

from core.serializers import UserProfileBasicSerializer
from library.models import Author, Book, BookLoan


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id', 'name', 'gender', 'created_at'
        )


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id', 'author', 'title', 'description', 'genre', 'publisher',
            'published_date', 'created_at', 'updated_at'
        )


class BookLoanSerializer(serializers.ModelSerializer):
    request_by = UserProfileBasicSerializer(read_only=True)
    approved_by = UserProfileBasicSerializer(read_only=True)

    class Meta:
        model = BookLoan
        fields = (
            'id', 'book', 'request_by', 'approved_by', 'approved_date',
            'repayment_date', 'created_at', 'updated_at'
        )

    def create(self, validated_data):
        with transaction.atomic():
            instance = super(BookLoanSerializer, self).create(validated_data=validated_data)
            instance.request_by_id = self.initial_data.get('request_by')
            instance.approved_by_id = self.initial_data.get('approved_by')
            instance.save()
            return instance
