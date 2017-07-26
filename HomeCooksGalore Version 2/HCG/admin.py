from django.contrib import admin
from .models import Dish,Upvote,Follow,Message
# Register your models here.

admin.site.register(Dish)
admin.site.register(Upvote)
admin.site.register(Follow)
admin.site.register(Message)