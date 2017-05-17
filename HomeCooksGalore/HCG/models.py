from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
# Create your models here.

class Dish(models.Model):
    dishName = models.CharField(max_length = 250)
    dishRating = models.IntegerField(default=0)
    dishPublisher = models.ForeignKey(User)
    dishCategory = models.CharField(max_length=10,choices=(('Food','Food'),('Drink','Drink')))
    dishSteps = models.TextField(max_length = 1000)
    dishFavourited = models.BooleanField(default=False)
    dishCoverImage = models.FileField()

    def get_absolute_url(self):
        return '/HCG'

    def __str__(self):
        return self.dishName + '-' + self.dishPublisher.username