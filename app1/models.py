from django.db import models

from django.conf import settings

DEFAULT_TYPE = 1
TYPE_CHOICES = (
    (1, 'fundacja'),
    (2, 'organizacja pozarzadowa'),
    (3, 'zbiorka lokalna'),
)


class Category(models.Model):
    '''Kategoria np'''
    name = models.CharField(max_length=255)


class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=DEFAULT_TYPE)
    categories = models.ManyToManyField(Category, related_name='institutions')


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category, related_name='donations')
    institution = models.ForeignKey(Institution, related_name='donations', on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=12)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

