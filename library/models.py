from django.db import models

from core.models import BaseEntity


class Author(BaseEntity):
    user = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, related_name='author')
    name = models.CharField(max_length=64, null=True)
    gender = models.CharField(max_length=16, null=True)
    website = models.URLField(null=True)

    class Meta:
        app_label = 'library'


class Book(BaseEntity):
    author = models.ForeignKey('library.Author', on_delete=models.SET_NULL, null=True, related_name='books')
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=32, null=True, blank=True)
    publisher = models.CharField(max_length=64, null=True, blank=True)
    published_date = models.DateField(null=True)

    class Meta:
        app_label = 'library'


class BookLoan(BaseEntity):
    book = models.ForeignKey('library.Book', on_delete=models.SET_NULL, null=True, related_name='book_loans')
    request_by = models.ForeignKey(
        'core.UserProfile', on_delete=models.SET_NULL, null=True, related_name='req_book_loans')
    approved_by = models.ForeignKey(
        'core.UserProfile', on_delete=models.SET_NULL, null=True, related_name='approve_book_loans')
    approved_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    repayment_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

    class Meta:
        app_label = 'library'
