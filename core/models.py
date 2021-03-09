from django.db import models
from django.contrib.auth.models import User


class BaseEntity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        app_label = 'core'
        abstract = True

class UserProfile(BaseEntity):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
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
