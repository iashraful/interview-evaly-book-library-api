from rest_framework import status

from core.models import UserProfile
from core.tests.base import LibraryManagementBaseTestCase


class CoreAPIEndpointTestCase(LibraryManagementBaseTestCase):
    def test_get_login_user(self):
        _username = self.login_admin_user()
        response = self.client.get(path='/api/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], _username)

    def test_put_login_user(self):
        _username = self.login_admin_user()
        _profile = UserProfile.objects.filter(user__username=_username).first()
        _data = {
            'id': _profile.pk,
            'full_name': 'Admin User',
            'role': self.member_role.id  # Update the role from admin to member
        }
        response = self.client.put(path='/api/me/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], _username)
        self.assertEqual(response.data['full_name'], 'Admin User')
        self.assertEqual(response.data['role'], self.member_role.id)

    def test_post_user_registration(self):
        _data = {
            'username': 'new_user',
            'password': self.common_passwd,
            'confirm_password': self.common_passwd,
            'role': self.member_role.id,
            'full_name': 'New User',
        }
        response = self.client.post(path='/api/user-registration/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], 'New User')
        self.assertEqual(response.data['role'], self.member_role.id)
        # Now login with the newly created user
        login_response = self.client.post(path='/api/jwt-token/', data={
            'username': 'new_user',
            'password': self.common_passwd
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in login_response.data)

    def test_get_role_api(self):
        self.login_admin_user()
        response = self.client.get(path='/api/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))

    def test_post_role_api(self):
        self.login_admin_user()
        _data = {
            'name': 'New Test Role'
        }
        response = self.client.post(path='/api/roles/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data['name'], 'New Test Role')

    def test_put_role_api(self):
        # Get data first
        self.login_admin_user()
        response = self.client.get(path='/api/roles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data['results'], list))
        _pk = response.data['results'][0]['id'] # Getting the first object PK
        _old_name = response.data['results'][0]['name'] # Getting the first object old name
        _data = {
            'id': _pk,
            'name': 'New Test Role'
        }
        response = self.client.put(path=f'/api/roles/{_pk}/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, dict))
        self.assertNotEqual(response.data['name'], _old_name) # not matched with old name
        self.assertEqual(response.data['name'], 'New Test Role') # Updated name matched
