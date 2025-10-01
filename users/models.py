import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    """
    Custom User model where email is the primary identifier for authentication.
    Username is still present but not required and not unique.
    The primary key is a UUID.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Make username optional and not unique
    username = models.CharField(
        _("username"), max_length=150, blank=True, null=True, unique=False
    )
    email = models.EmailField(_("email address"), unique=True)

    # Set email as the main field for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
