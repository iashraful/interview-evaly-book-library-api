from copy import deepcopy

from rest_framework import status

from core.tests.base import LibraryManagementBaseTestCase
from library.models import Author, Book


class BookAPIEndpointTestCase(LibraryManagementBaseTestCase):
    def setUp(self) -> None:
        super(BookAPIEndpointTestCase, self).setUp()
        # Create an author for test
        self.author = Author(name='Ashraful Islam', gender='Male')
        self.author.save()
        # Create book for further testing help
        self.initial_book_data = {
            'title': 'Introduction to Docker',
            'author': self.author,
            'description': 'It\'s a docker learning book for beginner.',
            'genre': 'Programming',
            'publisher': 'Packt Pub.',
            'published_date': '2018-03-06'
        }
        self.book = Book(**self.initial_book_data)
        self.book.save()

    def test_delete_book_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.delete(path=f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Login as member user
        self.login_member_user()
        response = self.client.delete(path=f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_book_api(self):
        self.login_admin_user()
        response = self.client.get(path='/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

        # Login as member user
        self.login_member_user()
        response = self.client.get(path='/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

    def test_post_book_api(self):
        self.login_admin_user()
        _data = deepcopy(self.initial_book_data)
        _data['author'] = self.book.author_id
        response = self.client.post(path='/api/books/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['title'], _data['title'])
        self.assertEqual(response.data['author'], self.author.pk)
        self.assertEqual(response.data['genre'], _data['genre'])
        self.assertEqual(response.data['published_date'], _data['published_date'])

        # Login as member user
        self.login_member_user()
        _data = deepcopy(self.initial_book_data)
        _data['author'] = self.book.author_id
        response = self.client.post(path='/api/books/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_book_api(self):
        self.login_admin_user()
        _data = deepcopy(self.initial_book_data)
        _data['title'] = 'This is Test Title'
        _data['author'] = self.book.author_id
        _data['description'] = 'This is Test Description'
        response = self.client.put(path=f'/api/books/{self.book.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertNotEqual(response.data['title'], self.initial_book_data['title'])  # not matched with old title
        self.assertNotEqual(response.data['description'],
                            self.initial_book_data['description'])  # not matched with old description
        self.assertEqual(response.data['title'], _data['title'])  # Updated name matched
        self.assertEqual(response.data['description'], _data['description'])  # Updated name matched

        # Login as member user
        self.login_member_user()
        _data = deepcopy(self.initial_book_data)
        _data['title'] = 'This is Test Title'
        _data['author'] = self.book.author_id
        _data['description'] = 'This is Test Description'
        response = self.client.put(path=f'/api/books/{self.book.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
