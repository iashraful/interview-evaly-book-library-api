from django.urls import path

from library.views.author_views import AuthorViewset
from library.views.book_loan_views import BookLoanViewset, BookLoanApproveView, BookLoanRejectView
from library.views.book_views import BookViewset

urlpatterns = [
    path('authors/', AuthorViewset.as_view({'get': 'list', 'post': 'create'}), name='authors'),
    path('authors/<int:pk>/', AuthorViewset.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='author_details'),

    path('books/', BookViewset.as_view({'get': 'list', 'post': 'create'}), name='books'),
    path('books/<int:pk>/', BookViewset.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book_details'),

    path('book-loans/', BookLoanViewset.as_view({'get': 'list', 'post': 'create'}), name='book_loans'),
    path('book-loans/<int:pk>/', BookLoanViewset.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book_loan_details'),

    path('book-loans/<int:pk>/approve/', BookLoanApproveView.as_view({'put': 'update',}), name='book_loan_approve'),
    path('book-loans/<int:pk>/reject/', BookLoanRejectView.as_view({'put': 'update',}), name='book_loan_reject'),
]
