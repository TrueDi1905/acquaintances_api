from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

SEX_CHOICES = [
    (0, 'Male'),
    (1, 'Female')
]


class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to='avatars/')
    sex = models.IntegerField(choices=SEX_CHOICES)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30,)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    lat = models.FloatField(default=59.9386)
    lon = models.FloatField(default=30.3141)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Like(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="client")
    client_like = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="client_like")
    constraints = [
        models.UniqueConstraint(
            fields=['client', 'client_like'],
            name='unique_follow',
        ),
    ]
