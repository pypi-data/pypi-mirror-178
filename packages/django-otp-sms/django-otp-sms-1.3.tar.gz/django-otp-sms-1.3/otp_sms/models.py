# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time
from binascii import unhexlify
from django.db import models
from django.utils.module_loading import import_string
from django.utils.six import python_2_unicode_compatible
from django.utils.encoding import force_text
from django_otp.oath import TOTP
from django_otp.util import random_hex, hex_validator
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .conf import settings


def default_key():
    return force_text(random_hex(20))


def key_validator(value):
    return hex_validator(20)(value)


@python_2_unicode_compatible
class SMSDevice(models.Model):
    number = PhoneNumberField(
        verbose_name=_("Phone number"),
        help_text=_("The mobile number to deliver tokens to.")
    )

    key = models.CharField(
        max_length=40,
        validators=[key_validator],
        default=default_key,
        help_text=_("A random key used to generate tokens (hex-encoded).")
    )

    code = models.CharField(
        max_length=10,
        null=True,
        help_text=_("The code to verify call")
    )

    last_t = models.BigIntegerField(
        default=-1,
        help_text=_("The t value of the latest verified token. The next token must be at a higher time step.")
    )

    class Meta(object):
        verbose_name = _("SMS Device")

    def __str__(self):
        return '%s' % self.number

    @classmethod
    def get(cls, request, number):
        device_id = request.session.get(settings.OTP_SMS_SESSION_KEY_DEVICE_ID)
        device = None
        if device_id:
            try:
                device_id = int(device_id)
            except ValueError:
                device_id = None
            try:
                device = cls._default_manager.get(pk=device_id, number=number)
            except cls.DoesNotExist:
                pass
        return device

    @property
    def bin_key(self):
        return unhexlify(self.key.encode())

    def generate_token(self, deliver=True, by_call=False):
        adapter_class = import_string(settings.OTP_SMS_ADAPTER)
        adapter = adapter_class(settings.OTP_SMS_AUTH)
        digits = self.get_totp_digits(adapter, by_call)
        totp = self.totp_obj(digits=digits)
        token = format(totp.token(), '0{}d'.format(digits))

        if deliver and not settings.OTP_SMS_TEST_MODE:
            if by_call:
                self.code = adapter.call(self.number, token)
                if self.code:
                    token = self.code
                    self.save(update_fields=['code'])
            else:
                message = settings.OTP_SMS_TOKEN_TEMPLATE.format(token=token)
                adapter.send(self.number, message, sender=settings.OTP_SMS_FROM)
        return token

    def verify_token(self, token, by_call=False):
        if settings.OTP_SMS_TEST_MODE:
            return True

        origin_token = token
        try:
            token = int(token)
        except ValueError:
            verified = False
        else:
            adapter_class = import_string(settings.OTP_SMS_ADAPTER)
            adapter = adapter_class(settings.OTP_SMS_AUTH)
            digits = self.get_totp_digits(adapter, by_call)
            totp = self.totp_obj(digits=digits)
            tolerance = settings.OTP_SMS_TOKEN_VALIDITY

            for offset in range(-tolerance, 1):
                totp.drift = offset
                if (totp.t() > self.last_t) and ((totp.token() == token) or (self.code and self.code == origin_token)):
                    self.last_t = totp.t()
                    self.save()

                    verified = True
                    break
            else:
                verified = False

        return verified

    def totp_obj(self, digits=6):
        totp = TOTP(self.bin_key, step=1, digits=digits)
        totp.time = time.time()

        return totp

    def get_totp_digits(self, adapter, by_call=False):
        return adapter.call_digits() if by_call else 6
