from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from common.mixins import TimeStamp
from django.conf import settings
from riders.models import Rider
from common import validators
from common import choices


# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(3)])
    description = models.TextField(max_length=500, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Garage(TimeStamp):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='garages')
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(3)])
    description = models.TextField(max_length=1000, validators=[MinLengthValidator(20)])
    city = models.CharField(max_length=100, choices = choices.BulgarianCityChoices.choices,)
    address = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    phone_number = models.CharField(max_length=50, validators=[validators.validate_phone_number,])
    email = models.EmailField(blank=True)
    services = models.ManyToManyField(Service, related_name='service_garages')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class GarageReview(TimeStamp):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='garage_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.garage.name} - {self.rating} / 5'

    class Meta:
        ordering = ('-created_at',)

        constraints = [
            models.UniqueConstraint(
                fields=['garage', 'reviewer'],
                name='unique_garage_review',
            )
        ]


