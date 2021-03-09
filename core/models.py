from django.db import models
from django.contrib.auth.models import User


class BaseEntity(models.Model):
    '''
    The BaseEntity is for multiple inheritance. Sometimes we need to inherit mixins and other classes on every model.
    In this case we are going to use this class on every model and extends everything on here.
    Also the global methods can be written here.
    '''
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        app_label = 'core'
        abstract = True


class Role(BaseEntity):
    name = models.CharField(max_length=32)

    class Meta:
        app_label = 'core'


class UserProfile(BaseEntity):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    role = models.ForeignKey('core.Role', on_delete=models.SET_NULL, null=True, related_name='user_profile')
    full_name = models.CharField(max_length=64, null=True)
    photo = models.ImageField(null=True)

    class Meta:
        app_label = 'core'

    def save(self, **kwargs):
        if not self.full_name:
            self.full_name = f'{self.user.first_name} {self.user.last_name}'
        super(UserProfile, self).save(**kwargs)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def username(self):
        return self.user.username
