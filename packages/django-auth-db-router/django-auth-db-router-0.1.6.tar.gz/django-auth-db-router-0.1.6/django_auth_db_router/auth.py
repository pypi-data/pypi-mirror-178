import binascii
import os
import random
import datetime

import pytz
from django.contrib.auth import get_user_model

from django.db import models
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token as AuthToken
from django.utils.translation import gettext_lazy as _


User = get_user_model()

utc = pytz.timezone(settings.TIME_ZONE)


class Token(AuthToken):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.OneToOneField(
        User, related_name='auth_token',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    last_use = models.DateTimeField(_("Last use"), auto_now=True)
    verification_code = models.CharField(max_length=5, null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    authenticated = models.BooleanField(default = False)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        managed = False
        db_table = 'AUTHENTICATION_TOKEN'

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super(AuthToken, self).save(force_insert, force_update)

    def activate(self, *args, **kwargs):
        self.authenticated = True

    def deactivate(self, *args, **kwargs):
        self.authenticated = False

    def generate_code(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        self.verification_code = code_string
        self.expiry_date = datetime.datetime.now() + datetime.timedelta(minutes=1)
        super().save(*args, **kwargs)


class ExpiringTokenAuthentication(TokenAuthentication):
    model = Token
    keyword = 'Bearer'

    def authenticate_credentials(self, key, request=None):
        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed({"error": "Invalid or Inactive Token", "is_authenticated": False})

        if not token.user.is_active:
            raise AuthenticationFailed({"error": "Invalid user", "is_authenticated": False})

        if not token.authenticated:
            raise AuthenticationFailed({"error": "Inactive Token", "is_authenticated": False})

        now = datetime.datetime.now().replace(tzinfo=utc)

        if token.last_use < now - settings.TOKEN_TTL:
            token.deactivate()
            token.save()
            raise AuthenticationFailed({"error": "Token has expired", "token_status": False})

        token.last_use = now
        token.save()
        return token.user, token


def custom_create_token(token_model, user, serializer):
    token = token_model.objects.create(user=user)
    now = datetime.datetime.now()
    token.created = now
    token.save()
    return token

