import binascii
import datetime
import os
import random
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token as AuthToken


User = get_user_model()


class Manager(models.Manager):
    """ Base manager with the following additions:
        - 'existing()' method that filters queryset by 'is_deleted=False'
    """
    def get_queryset(self):
        return super(Manager, self).get_queryset()

    def existing(self):
        return self.filter(is_deleted=False)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class Model(models.Model):
    """ Base model with the following additions:
        - uuid4 as object id;
        - created_at as object creation time;
        - updated_at as object last update time;
        - is_deleted as indicator that object is deleted or not;
     """

    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, editable=False)
    is_deleted = models.BooleanField(_('is deleted'), default=False)

    objects = Manager()

    class Meta:
        abstract = True


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
