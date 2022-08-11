from django.db import models
from django.core.validators import MinValueValidator, \
    MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(unique=True, max_length=100)

    # validators for make limitation on the value of the field
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self):
        return self.code
