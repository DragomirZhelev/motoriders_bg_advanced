from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

from common import validators


# Create your models here.

class AppUser(AbstractUser):
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), validators.validate_names_only_letters],)
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), validators.validate_names_only_letters],)
    email = models.EmailField(blank=True, null=True, unique=True)


    def __str__(self):
        return self.get_full_name()


