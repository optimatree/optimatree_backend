import binascii
from datetime import time
import os
from utils.exceptions import EmailUnverifiedError

from django.db import models
from django.contrib.auth.models import User
from django.db.models import indexes
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class AuthToken(models.Model):
    token_length = 40
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(
        _("Token"), max_length=token_length, unique=True, db_index=True)
    refresh_token = models.CharField(
        _("Refresh_token"), max_length=token_length, unique=True, db_index=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires = models.DateTimeField(_("Expires"))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_random_token()

        if not self.refresh_token:
            self.refresh_token = self.generate_random_token()

        if self.user is not None and self.user.is_active:
            self.created = timezone.now()
            self.expires = self.created.replace(year=self.created.year + 1)

            return super().save(*args, **kwargs)
        else:
            raise EmailUnverifiedError

    def refresh(self):
        self.token = self.generate_random_token()
        self.refresh_token = self.generate_random_token()
        
        self.save()

    def revoke(self):
        self.delete()

    def get_new_refresh_token(self):
        self.refresh_token = self.generate_random_token()
        self.save()

    def generate_random_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def is_expired(self):
        return self.expires.timestamp() <= self.created.timestamp()

    def __str__(self):
        return self.token

    def to_dict(self) -> dict:
        return {
            'access_token': self.token,
            'refresh_token': self.refresh_token,
            'expires': self.expires,
        }
