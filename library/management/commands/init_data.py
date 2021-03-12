import sys

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils import timezone

from core.enums import RoleEnum
from core.models import Role, UserProfile
from library.models import Author, Book, BookLoan
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_roles(*args, **options)
        self.create_user_profiles(*args, **options)
        self.create_authors(*args, **options)
        self.create_books(*args, **options)
        self.create_book_loans(*args, **options)

    def create_roles(self, *args, **kwargs):
        self.stdout.write('Creating Roles...')
        for e in RoleEnum:
            Role.objects.get_or_create(name=e.name, type=e.value)
        self.stdout.write('Done.\n')

    def create_user_profiles(self, *args, **kwargs):
        self.stdout.write('Creating Admin Users...')
        admin_users = ['ashraful', 'admin']
        admin_role = Role.objects.filter(type=RoleEnum.Admin.value).first()
        for username in admin_users:
            _user, _created = User.objects.get_or_create(username=username)
            if _user:
                _user.set_password(raw_password='1234')
                _user.save()
                _profile, _created = UserProfile.objects.get_or_create(user_id=_user.pk, role_id=admin_role.pk)

        self.stdout.write('Done.\n')
        self.stdout.write('Creating Member Users...')
        # Creating member user
        member_users = ['john', 'clark']
        member_role = Role.objects.filter(type=RoleEnum.Member.value).first()
        for username in member_users:
            _user, _created = User.objects.get_or_create(username=username)
            if _user:
                _user.set_password(raw_password='1234')
                _user.save()
                _profile, _created = UserProfile.objects.get_or_create(user_id=_user.pk, role_id=member_role.pk)
        self.stdout.write('Done.\n')

    def create_authors(self, *args, **kwargs):
        self.stdout.write('Creating Authors Users...')
        authors = ['test_author', 'ahamed']
        for author_name in authors:
            _user, _created = User.objects.get_or_create(username=author_name)
            if _created:
                _user.set_password(raw_password='1234')
                _user.save()
                self.author = Author(name=faker.name(), gender='Male')
                self.author.user = _user
                self.author.save()
        self.stdout.write('Done.\n')

    def create_books(self, *args, **kwargs):
        self.stdout.write('Creating Books...')
        _authors = Author.objects.all()
        for _ in range(1000):
            Book.objects.get_or_create(
                title=faker.name(),
                description='A fake book created by Faker.',
                author=_authors[faker.random_int(0, 1)],
                genre='Test',
                publisher=faker.word(),
                published_date=timezone.now().replace(
                    year=int(faker.year()), month=int(faker.month()))
            )
        self.stdout.write('Done.\n')

    def create_book_loans(self, *args, **kwargs):
        self.stdout.write('Creating Book Loans...')
        books = Book.objects.all()
        admin_users = UserProfile.objects.filter(role__type=RoleEnum.Admin.value)
        member_users = UserProfile.objects.filter(role__type=RoleEnum.Member.value)
        for _ in range(0, 700):
            BookLoan.objects.get_or_create(
                book=books[faker.random_int(0, 999)],
                request_by=member_users[faker.random_int(0, 1)],
                action_taken_by=admin_users[faker.random_int(0, 1)],
                status=faker.random_int(1, 2),
                action_date=timezone.now().replace(year=int(faker.year()), month=int(faker.month())),
                created_at=timezone.now().replace(month=int(faker.month())),
                repayment_date=timezone.now().replace(year=int(faker.year()), month=int(faker.month())),
            )
        self.stdout.write('Done.\n')

