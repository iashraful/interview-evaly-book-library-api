from django.contrib.auth.models import User
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import UserProfile, Role


class UserRegistrationSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 'username', 'role', 'password', 'confirm_password', 'full_name', 'created_at'
        )
        read_only_fields = (
            'id', 'created_at'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({'non_field_errors': [_('Password and Confirm password are not matching.')]})
        return super(UserRegistrationSerializer, self).validate(attrs=attrs)

    def create(self, attrs):
        with transaction.atomic():
            full_name = attrs['full_name']
            role = attrs['role']
            _first_name = full_name.split(' ')[0]
            _last_name = ' '.join(full_name.split(' ')[1::])
            user = User.objects.create(
                username=attrs['username'], first_name=_first_name, last_name=_last_name)
            if user:
                user.set_password(raw_password=attrs['password'])
                user.save()
                profile = UserProfile(user=user, full_name=full_name, role=role)
                profile.save()
                return profile


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id', 'role', 'full_name', 'first_name', 'last_name',
            'username', 'email', 'created_at', 'updated_at', 'photo'
        )
        read_only_fields = ('first_name', 'last_name', 'username', 'email',)

    def update(self, instance, validated_data):
        instance = super(LoginUserSerializer, self).update(instance=instance, validated_data=validated_data)
        _user = instance.user
        if 'first_name' in self.initial_data:
            _user.first_name = self.initial_data['first_name']
        if 'last_name' in self.initial_data:
            _user.last_name = self.initial_data['last_name']
        if 'email' in self.initial_data:
            _user.email = self.initial_data['email']
        _user.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'created_at', 'updated_at', )
