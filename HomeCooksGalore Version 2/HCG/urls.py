"""HomeCooksGalore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from . import views
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
    url(r'^loginPage/$', views.LoginPage),
    url(r'^registerPage/$',views.UserFormView.as_view()),
    url(r'^logout/$', views.Logout),

    url(r'^(?P<pk>[0-9]+)/$',views.DishDetails),
    url(r'^$',views.MyDishes),
    url(r'^foods/$',views.AllFoods),
    url(r'^drinks/$',views.AllDrinks),

    url(r'^displayDishes/(?P<mode>[0-9]+)/$',views.DisplayDishes),
    url(r'^addDish$',login_required(views.DishCreate.as_view())),
    url(r'^updateDish/(?P<pk>[0-9]+)/$',login_required(views.DishUpdate.as_view())),
    url(r'^deleteDish/(?P<pk>[0-9]+)/$',login_required(views.DishDelete.as_view())),

    url(r'^upvoteDish/(?P<pk>[0-9]+)/$',login_required(views.UpvoteCreate)),

    url(r'^profile/$',login_required(views.ViewProfile)),
    url(r'^followUser/(?P<pk>[0-9]+)/$',login_required(views.FollowUser)),
    url(r'draftMessage/(?P<pk>[0-9]+)/$',login_required(views.MessageCreateForm)),
    url(r'^createMessage/$',login_required(views.MessageCreate)),
    url(r'^messages/$',login_required(views.ViewMessagesSummaries)),
    url(r'^messageDetails/$',login_required(views.ViewMessages)),

    url(r'^ajax/followUnfollow/$',login_required(views.FollowUnfollow)),
    url(r'^ajax/likeUnlike/$',login_required(views.LikeUnlike)),

]
