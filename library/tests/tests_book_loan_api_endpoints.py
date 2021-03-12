from copy import deepcopy
from datetime import timedelta
from django.utils import timezone

from rest_framework import status

from core.models import UserProfile
from core.tests.base import LibraryManagementBaseTestCase
from library.enums import BookLoanStatusEnum
from library.models import Book, Author, BookLoan


class BookLoanAPIEndpointTestCase(LibraryManagementBaseTestCase):
    def setUp(self) -> None:
        super(BookLoanAPIEndpointTestCase, self).setUp()
        # Create an author for test
        self.author = Author(name='Ashraful Islam', gender='Male')
        self.author.save()
        self.admin_user = UserProfile.objects.filter(user__username='admin').first()
        self.member_user = UserProfile.objects.filter(user__username='john').first()
        # Create book for further testing help
        _book_data = {
            'title': 'Introduction to Docker',
            'author': self.author,
            'description': 'It\'s a docker learning book for beginner.',
            'genre': 'Programming',
            'publisher': 'Packt Pub.',
            'published_date': timezone.now().replace(year=2010)
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
        # Login as admin user
        self.login_admin_user()
        response = self.client.delete(path=f'/api/book-loans/{self.book_loan.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Login as member user
        self.login_member_user()
        response = self.client.delete(path=f'/api/book-loans/{self.book_loan.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_book_loan_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.get(path='/api/book-loans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

        # Login as member user
        self.login_member_user()
        response = self.client.get(path='/api/book-loans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

    def test_post_book_loan_api(self):
        # Login as admin user
        self.login_admin_user()
        _data = deepcopy(self.initial_book_loan_data)
        _data['book'] = self.book.pk
        response = self.client.post(path='/api/book-loans/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['book'], self.book.id)
        self.assertEqual(response.data['request_by']['id'], self.admin_user.pk)

        # Login as member user
        self.login_member_user()
        _data = deepcopy(self.initial_book_loan_data)
        _data['book'] = self.book.pk
        response = self.client.post(path='/api/book-loans/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book'], self.book.id)
        # It'll automatically set the requested user
        self.assertEqual(response.data['request_by']['id'], self.member_user.pk)

    def test_put_book_loan_api(self):
        # Login as admin user
        self.login_admin_user()
        _data = deepcopy(self.initial_book_loan_data)
        _data['book'] = self.book.pk
        _data['repayment_date'] = timezone.now() + timedelta(days=1)
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))

        # Login as member user
        self.login_member_user()
        _data = deepcopy(self.initial_book_loan_data)
        _data['book'] = self.book.pk
        _data['repayment_date'] = timezone.now() + timedelta(days=1)
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_loan_approve_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/approve/', data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['action_taken_by']['id'], self.admin_user.pk)
        self.assertEqual(response.data['status'], BookLoanStatusEnum.Approved.value)

        # Login as member user
        self.login_member_user()
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/approve/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_loan_reject_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/reject/', data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['action_taken_by']['id'], self.admin_user.pk)
        self.assertEqual(response.data['status'], BookLoanStatusEnum.Rejected.value)

        # Login as member user
        self.login_member_user()
        response = self.client.put(path=f'/api/book-loans/{self.book_loan.id}/reject/', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_loan_export_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.get(path=f'/api/book-loans/export/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertTrue(response.data['path'].startswith('/media/exported_files/'))

        # Login as member user
        self.login_member_user()
        response = self.client.get(path=f'/api/book-loans/export/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
