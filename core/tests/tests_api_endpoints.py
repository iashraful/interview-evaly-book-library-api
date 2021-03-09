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
            'role': self.member_role.id
        }
        response = self.client.put(path='/api/me/', data=_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], _username)
        self.assertEqual(response.data['full_name'], 'Admin User')
        self.assertEqual(response.data['role'], self.member_role.id)

