from copy import deepcopy
from datetime import datetime, timedelta

from rest_framework import status

from core.models import UserProfile
from core.tests.base import LibraryManagementBaseTestCase
from library.models import Book, Author, BookLoan


class BookLoanAPIEndpointTestCase(LibraryManagementBaseTestCase):
    def setUp(self) -> None:
        super(BookLoanAPIEndpointTestCase, self).setUp()
        # Create an author for test
        self.author = Author(name='Ashraful Islam', gender='Male')
        self.author.save()
        self.admin_user = UserProfile.objects.filter(user__username='admin').first()
        self.member_user = UserProfile.objects.filter(user__username='nick').first()
        # Create book for further testing help
        _book_data = {
            'title': 'Introduction to Docker',
            'author': self.author,
            'description': 'It\'s a docker learning book for beginner.',
            'genre': 'Programming',
            'publisher': 'Packt Pub.',
            'published_date': datetime.now().replace(year=2010)
        }
        self.book = Book(**_book_data)
        self.book.save()
        # Create a book loan
        self.initial_book_loan_data = {
            'book': self.book,
            'request_by': self.member_user
        }
        self.book_loan = BookLoan(**self.initial_book_loan_data)
        self.book_loan.save()

    def test_delete_book_loan_api(self):
        self.login_admin_user()
        response = self.client.delete(path=f'/api/book-loans/{self.book_loan.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_book_loan_api(self):
        self.login_admin_user()
        response = self.client.get(path='/api/book-loans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

    def test_post_book_loan_api(self):
        self.login_admin_user()
        _data = deepcopy(self.initial_book_loan_data)
        _data['book'] = self.book.pk
        _data['request_by'] = self.member_user.pk
        response = self.client.post(path='/api/book-loans/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['book'], self.book.id)
        self.assertEqual(response.data['request_by']['id'], self.member_user.pk)

    def test_put_book_loan_api(self):
        self.login_admin_user()
        _data = deepcopy(self.initial_book_loan_data)
        _data['book'] = self.book.pk
        _data['request_by'] = self.member_user.pk
        _data['approved_by'] = self.admin_user.pk
        _data['approved_date'] = datetime.now() - timedelta(days=10)
        _data['repayment_date'] = datetime.now() + timedelta(days=1)
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['approved_by']['id'], self.admin_user.pk)
