from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.test import APIJWTClient

from core.enums import RoleEnum
from core.models import Role, UserProfile

ROLE_VS_USERS = [
    {
        'role': 'Admin',
        'users': ['admin', 'ashraful']
    },
    {
        'role': 'Member',
        'users': ['nick', 'john']
    },
]


class LibraryManagementBaseTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIJWTClient()

        # Common values
        self.common_passwd = '1234'
        self.member_role = None
        self.admin_role = None

        # Creating Roles and Users
        for data in ROLE_VS_USERS:
            role_name = data['role']
            role = None
            if role_name == 'Admin':
                role, _created = Role.objects.get_or_create(name=role_name, type=RoleEnum.Admin.value)
                self.admin_role = role
            if role_name == 'Member':
                role, _created = Role.objects.get_or_create(name=role_name, type=RoleEnum.Member.value)
                self.member_role = role
            if not role:
                continue
            for username in data['users']:
                _user, _created = User.objects.get_or_create(username=username)
                if _user:
                    _user.set_password(raw_password=self.common_passwd)
                    _user.save()
                    _profile, _created = UserProfile.objects.get_or_create(user_id=_user.pk, role_id=role.pk)
        # END Creating roles and users

        # Login user according to Role
        self.admin_user_token = None
        self.member_user_token = None

    def login_admin_user(self):
        '''
        This is a helper method for the base class. We will use this where necessary to login a admin user
        '''
        _username = 'admin'
        response = self.client.post(path='/api/jwt-token/', data={
            'username': _username,
            'password': self.common_passwd
        })
        if response.status_code == status.HTTP_200_OK:
            self.admin_user_token = response.data['token']
            self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.admin_user_token))
        return _username

    def login_member_user(self):
        '''
        This is a helper method for the base class. We will use this where necessary to login a member user
        '''
        _username = 'john'
        response = self.client.post(path='/api/jwt-token/', data={
            'username': _username,
            'password': self.common_passwd
        })
        if response.status_code == status.HTTP_200_OK:
            self.member_user_token = response.data['token']
            self.client.credentials(HTTP_AUTHORIZATION='JWT {0}'.format(self.member_user_token))
        return _username
