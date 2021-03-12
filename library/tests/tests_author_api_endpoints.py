from copy import deepcopy
from django.contrib.auth.models import User

from rest_framework import status

from core.tests.base import LibraryManagementBaseTestCase
from library.models import Author


class AuthorAPIEndpointTestCase(LibraryManagementBaseTestCase):
    def setUp(self) -> None:
        super(AuthorAPIEndpointTestCase, self).setUp()
        # Create an author for test
        self.initial_author_data = {
            'name': 'Iron Fist',
            'gender': 'Male',
            'username': 'iron_fist',
            'password': self.common_passwd,
            'confirm_password': self.common_passwd,
        }
        _user = User(username='ash_author')
        _user.set_password(raw_password=self.common_passwd)
        _user.save()
        self.author = Author(name='Ashraful Islam', gender='Male')
        self.author.user = _user
        self.author.save()

    def test_delete_author_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.delete(path=f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Login as member user
        self.login_member_user()
        response = self.client.delete(path=f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_author_api(self):
        # Login as admin user
        self.login_admin_user()
        response = self.client.get(path='/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

        # Login as member user
        self.login_member_user()
        response = self.client.get(path='/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

    def test_post_author_api(self):
        self.login_admin_user()
        _data = deepcopy(self.initial_author_data)
        response = self.client.post(path='/api/authors/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['name'], _data['name'])
        self.assertEqual(response.data['gender'], _data['gender'])

        # Login as member user
        self.login_member_user()
        _data = deepcopy(self.initial_author_data)
        response = self.client.post(path='/api/authors/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_author_api(self):
        self.login_admin_user()
        _data = deepcopy(self.initial_author_data)
        _data['name'] = 'Allison Argent'
        _data['gender'] = 'Female'
        response = self.client.put(path=f'/api/authors/{self.author.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertNotEqual(response.data['name'], self.author.name)  # not matched with old title
        self.assertNotEqual(response.data['gender'], self.author.gender)  # not matched with old description
        self.assertEqual(response.data['name'], _data['name'])  # Updated name matched
        self.assertEqual(response.data['gender'], _data['gender'])  # Updated name matched

        # Login as member user
        self.login_member_user()
        _data = deepcopy(self.initial_author_data)
        _data['name'] = 'Allison Argent'
        _data['gender'] = 'Female'
        response = self.client.put(path=f'/api/authors/{self.author.id}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
