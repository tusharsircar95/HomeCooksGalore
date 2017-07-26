from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Dish(models.Model):
    dishName = models.CharField(max_length = 250)
    dishRating = models.IntegerField(default=0)
    dishPublisher = models.ForeignKey(User)
    dishCategory = models.CharField(max_length=10,choices=(('Food','Food'),('Drink','Drink')))
    dishSteps = models.TextField(max_length = 5000)
    dishCoverImage = models.FileField()

    def get_absolute_url(self):
        return '/HCG'

    def __str__(self):
        return self.dishName + '-' + self.dishPublisher.username

class Upvote(models.Model):
    dish = models.ForeignKey(Dish)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.username + ' upvoted ' + self.dish.dishName

    @classmethod
    def create(cls,dish,user):
        upvote = cls(dish=dish,user=user)
        return upvote

class Follow(models.Model):
    follower = models.ForeignKey(User,related_name='follower')
    follows = models.ForeignKey(User,related_name='follows')

    def __str__(self):
        return self.follower.username + ' follows ' + self.follows.username

    @classmethod
    def create(cls, follower, follows):
        follow = cls(follower=follower, follows=follows)
        return follow


class Message(models.Model):
    sender = models.ForeignKey(User,related_name='sender')
    receiver = models.ForeignKey(User,related_name='receiver')
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.message + ' sent by ' + self.sender.username + ' to ' + self.receiver.username

    @classmethod
    def create(cls,message,sender,receiver):
        messageObject = cls(message=message,sender=sender,receiver=receiver,timestamp=datetime.now())
        return messageObject

'''
class Comment(models.Model):
    dish = models.ForeignKey(Dish)
    user = models.ForeignKey(User)
    commentText = models.TextField(max_length=1000)

    def __str__(self):
        return self.user.username + ' commented ' + "\"" + self.commentText + "\" on " + self.dish.dishName

    @classmethod
    def create(cls, dish, user, commentText):
        comment = cls(dish=dish, user=user, commentText=commentText)
        return comment

'''