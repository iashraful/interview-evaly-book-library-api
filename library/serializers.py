from django.db import transaction
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from core.serializers import UserProfileBasicSerializer, DjangoUserBasicSerializer
from library.models import Author, Book, BookLoan


class AuthorSerializer(serializers.ModelSerializer):
    user = DjangoUserBasicSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'user', 'gender', 'created_at')


class AuthorCreateSerializer(serializers.ModelSerializer):
    '''
    The serializer will be used for create author only.
    '''
    name = serializers.CharField(required=True)
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Author
        fields = (
            'id', 'username', 'password', 'confirm_password', 'name', 'gender', 'created_at'
        )
        read_only_fields = (
            'id', 'created_at'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({'non_field_errors': [_('Password and Confirm password are not matching.')]})
        return super(AuthorCreateSerializer, self).validate(attrs=attrs)

    def create(self, attrs):
        with transaction.atomic():
            full_name = attrs['name']
            gender = attrs['gender']
            _first_name = full_name.split(' ')[0]
            _last_name = ' '.join(full_name.split(' ')[1::])
            user = User.objects.create(
                username=attrs['username'], first_name=_first_name, last_name=_last_name)
            if user:
                user.set_password(raw_password=attrs['password'])
                user.save()
                author = Author(user=user, name=full_name, gender=gender)
                author.save()
                return author


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id', 'author', 'title', 'description', 'genre', 'publisher',
            'published_date', 'created_at', 'updated_at'
        )


class BookLoanSerializer(serializers.ModelSerializer):
    request_by = UserProfileBasicSerializer(read_only=True)
    approved_by = UserProfileBasicSerializer(read_only=True)

    class Meta:
        model = BookLoan
        fields = (
            'id', 'book', 'request_by', 'approved_by', 'approved_date',
            'repayment_date', 'created_at', 'updated_at',
        )

    def create(self, validated_data):
        with transaction.atomic():
            instance = super(BookLoanSerializer, self).create(validated_data=validated_data)
            instance.request_by_id = self.initial_data.get('request_by')
            instance.approved_by_id = self.initial_data.get('approved_by')
            instance.save()
            return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance = super(BookLoanSerializer, self).create(validated_data=validated_data)
            instance.request_by_id = self.initial_data.get('request_by')
            instance.approved_by_id = self.initial_data.get('approved_by')
            instance.save()
            return instance
