from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from .models import Dish,Upvote,Follow,Message
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm,RegisterForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
import operator
# Create your views here.


class DishListView(generic.ListView):
    template_name = 'HCG/dishListTemplate.html'
    context_object_name = 'dishList'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Dish.objects.all()
        return None

class DishDetailsView(generic.DetailView):
    model = Dish
    template_name = 'HCG/dishDetailTemplate.html'

class DishCreate(CreateView):
    model = Dish
    fields = ['dishName','dishSteps','dishCategory','dishCoverImage']

    def form_valid(self,form):
        form.instance.dishPublisher = self.request.user
        return super(DishCreate,self).form_valid(form)




class DishUpdate(UserPassesTestMixin,UpdateView):
    model = Dish
    fields = ['dishName','dishSteps','dishCategory','dishCoverImage']

    def test_func(self):
        return self.request.user.username == Dish.objects.get(pk=self.kwargs['pk']).dishPublisher.username

class DishDelete(UserPassesTestMixin,DeleteView):
    model = Dish
    success_url = '/HCG/'

    def test_func(self):
        return self.request.user.username == Dish.objects.get(pk=self.kwargs['pk']).dishPublisher.username

def UpvoteCreate(request,pk):
    dish = Dish.objects.get(pk=pk)
    if Upvote.objects.filter(dish=dish,user=request.user).count() == 0:
        upvote = Upvote.create(Dish.objects.get(pk=pk),request.user)
        upvote.save()
        dish.dishRating = dish.dishRating + 1
        dish.save()
    else:
        upvote = Upvote.objects.get(dish=dish,user=request.user)
        upvote.delete()
        dish.dishRating = dish.dishRating - 1
        dish.save()

    next = request.POST.get('next', '/HCG/')
    return HttpResponseRedirect(next)

class UserFormView(View):
    form_class = UserForm
    template_name = 'HCG/loginform.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form,'form_url':'/HCG/registerPage/','submitText':'Sign Up'})
        pass

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.username = username
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password,email=email)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/HCG/')

        return render(request,self.template_name,{'form':form, 'form_url':'/HCG/registerPage/','submitText':'Sign Up'})

def LoginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/HCG/')

    form = LoginForm()
    return render(request,'HCG/loginForm.html',{'form':form, 'form_url':'/HCG/loginPage/', 'submitText':'Sign In'})


def RegisterPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.username = username
            user.set_password(password)

            if User.objects.get(username=username) is None:
                user.save()
                user = authenticate(username=username,password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/HCG/')
            else: return HttpResponseRedirect('admin/')
    form = RegisterForm()
    return render(request,'HCG/loginForm.html',{'form':form, 'form_url':'/HCG/registerPage/'})


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/HCG/loginPage')

def MyDishes(request):

    if request.user.is_authenticated:
        if request.GET.get('q', '') != '':
            query = request.GET.get('q','')
            dishList = Dish.objects.filter(dishName__icontains=query)
            title = 'Search Results for ' + "'" + query + "'"

            user = request.user
            liked = []
            dishLikePairs = []
            for i in range(len(dishList)):
                liked.append(0)
                if Upvote.objects.filter(dish=dishList[i], user=user).count() == 1:
                    liked[i] = 1
                dishLikePairs.append((dishList[i], liked[i]))

            next = '/HCG/?q=' + query
            template = loader.get_template('HCG/homepageTemplate.html')
            context = {
                'dishList': dishList,
                'username': request.user.username,
                'title': title,
                'dishLikePairs' : dishLikePairs,
                'next' : next,
            }
            return HttpResponse(template.render(context, request))

        return HttpResponseRedirect('/HCG/displayDishes/0/')
    else:
        return HttpResponseRedirect('/HCG/loginPage')

def AllFoods(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/HCG/displayDishes/1')
    else:
        return HttpResponseRedirect('/HCG/loginPage')

def AllDrinks(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/HCG/displayDishes/2')
    else:
        return HttpResponseRedirect('/HCG/loginPage')

def DisplayDishes(request,mode):

    mode = int(mode)
    if mode < 0 or mode > 2:
        return HttpResponse(status=404)
    foodsActive = ''
    drinksActive = ''
    if request.user.is_authenticated:

        if mode == 0:
            dishList = Dish.objects.filter(dishPublisher=request.user)
            title = 'Your Recipies'
            next = '/HCG/'
        if mode == 1:
            dishList = Dish.objects.filter(dishCategory='Food')
            title = 'All Foods'
            next = '/HCG/foods/'
            foodsActive = 'active'

        if mode == 2:
            dishList = Dish.objects.filter(dishCategory='Drink')
            title = 'All Drinks'
            next = '/HCG/drinks/'
            drinksActive = 'active'

        user = request.user
        liked = []
        dishLikePairs = []
        for i in range(len(dishList)):
            liked.append(0)
            if Upvote.objects.filter(dish=dishList[i],user=user).count() == 1:
                liked[i] = 1
            dishLikePairs.append((dishList[i],liked[i]))


        template = loader.get_template('HCG/homepageTemplate.html')
        context = {
            'dishLikePairs': dishLikePairs,
            'username': request.user.username,
            'title': title,
            'next': next,
            'foodsActive' : foodsActive,
            'drinksActive' : drinksActive,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/HCG/loginPage')


def DishDetails(request,pk):

    if request.user.is_authenticated:
        dish = get_object_or_404(Dish,id=pk)
        template = loader.get_template('HCG/dishDetailTemplate.html')
        username = request.user.username
        context = {
            'dish': dish,
            'username': username
        }
        return HttpResponse(template.render(context, request))
    return HttpResponseRedirect('/HCG/loginPage')

def ViewProfile(request):
    username = request.GET.get('q','')
    if username == '':
        user = request.user
    else:
        userFilter = User.objects.filter(username=username)
        if userFilter.count() == 0:
            return HttpResponse(status=404)
        user = userFilter[0]

    template = loader.get_template('HCG/myProfileTemplate.html')
    dishList = Dish.objects.filter(dishPublisher=user)
    recipieCount = dishList.count()

    title = 'Uploaded Recipies'
    next = '/HCG/profile/?q=' + username

    liked = []
    dishLikePairs = []
    for i in range(len(dishList)):
        liked.append(0)
        if Upvote.objects.filter(dish=dishList[i], user=request.user).count() == 1:
            liked[i] = 1
        dishLikePairs.append((dishList[i], liked[i]))


    selfProfile = False
    if request.user == user:
        selfProfile = True

    if Follow.objects.filter(follower=request.user,follows=user).count() == 0:
        following = False
    else: following = True

    followerCount = Follow.objects.filter(follows=user).count();
    followsCount = Follow.objects.filter(follower=user).count();

    context = {
        'user' : user,
        'username' : request.user.username,
        'recipieCount' : recipieCount,
        'dishLikePairs': dishLikePairs,
        'title' : title,
        'next' : next,
        'selfProfile' : selfProfile,
        'following' : following,
        'followerCount' : followerCount,
        'followsCount' : followsCount,
    }
    return HttpResponse(template.render(context,request))

def FollowUser(request,pk):
    follows = User.objects.get(pk=pk)
    follower = request.user

    # User cannot follow himself
    if follows == follower:
        return HttpResponseRedirect('/HCG/profile/')

    # Create a follow object if user wasn't already following
    if Follow.objects.filter(follower=follower,follows=follows).count() == 0:
        follow = Follow.create(follower=follower,follows=follows)
        follow.save()
    else: # Unfollow user
        follow = Follow.objects.get(follower=follower,follows=follows)
        follow.delete()
    return HttpResponseRedirect('/HCG/profile/?q=' + follows.username)

def MessageCreateForm(request,pk):
    template = loader.get_template('HCG/message_form.html')
    context = {
        'receiverID' : pk,
    }
    return HttpResponse(template.render(context, request))

def MessageCreate(request):
    message = request.POST.get('message', '...')
    receiverID = int(request.POST.get('receiverID','0'))
    receiver = User.objects.get(pk=receiverID)
    sender = request.user
    messageObject = Message.create(message=message, sender=sender, receiver=receiver)
    messageObject.save()
    return HttpResponseRedirect('/HCG/messageDetails/?q=' + receiver.username)

def FollowUnfollow(request):
    pk = int(request.GET.get('followsID','0'))
    follows = User.objects.get(pk=pk)
    follower = request.user

    # User cannot follow himself
    if follows == follower:
        return HttpResponseRedirect('/HCG/profile/')

    # Create a follow object if user wasn't already following
    if Follow.objects.filter(follower=follower, follows=follows).count() == 0:
        follow = Follow.create(follower=follower, follows=follows)
        follow.save()
        responseText = 'followed'
    else:  # Unfollow user
        follow = Follow.objects.get(follower=follower, follows=follows)
        follow.delete()
        responseText = 'unfollowed'
    data = {
        'responseText' : responseText,
        'followerCount' : Follow.objects.filter(follows=follows).count(),
    }
    return JsonResponse(data)

def LikeUnlike(request):

    pk = request.GET.get('dishID','0')
    dish = Dish.objects.get(pk=pk)
    if Upvote.objects.filter(dish=dish, user=request.user).count() == 0:
        upvote = Upvote.create(Dish.objects.get(pk=pk), request.user)
        upvote.save()
        dish.dishRating = dish.dishRating + 1
        dish.save()
        responseText = 'liked'
        newRating = dish.dishRating
    else:
        upvote = Upvote.objects.get(dish=dish, user=request.user)
        upvote.delete()
        dish.dishRating = dish.dishRating - 1
        dish.save()
        responseText = 'unliked'
        newRating = dish.dishRating
    data = {
        'responseText' : responseText,
        'newRating' : newRating,
    }
    return JsonResponse(data)

def ViewMessagesSummaries(request):
    user = request.user;
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))

    uniqueUsers = list()
    for message in messages:
        uniqueUsers.append(message.sender)
        uniqueUsers.append(message.receiver)

    uniqueUsers.append(user)
    uniqueUsers = list(set(uniqueUsers))
    uniqueUsers.remove(user)


    class MessageSummary:

        def __init__(self,user,message,time,otherUser):
            self.user = user
            self.message = message
            self.time = time
            self.otherUser = otherUser

    l = len(messages)
    messageSummaries = list()
    for uniqueUser in uniqueUsers:
        conversation = messages.filter((Q(receiver=uniqueUser) & Q(sender=user)) | (Q(receiver=user) & Q(sender=uniqueUser)))
        conversation = sorted(conversation, key=operator.attrgetter('timestamp'))
        l = len(conversation)
        headerUser = conversation[l-1].sender
        headerMessage = conversation[l-1].message
        headerTime = conversation[l-1].timestamp
        messageSummaries.append(MessageSummary(headerUser,headerMessage,headerTime,uniqueUser))

    if len(messageSummaries) == 0:
        title = 'No messages yet!'
    else: title = 'Your Messages'

    template = loader.get_template('HCG/myMessagesSummaryTemplate.html')
    context = {
        'username': request.user.username,
        'messageSummaries' : messageSummaries,
        'title' : title,
    }
    return HttpResponse(template.render(context, request))


def ViewMessages(request):
    user = request.user;
    otherUsername = request.GET.get('q', '')
    if(User.objects.filter(username=otherUsername).count() == 0 or user.username == otherUsername):
        return HttpResponse(status=404)
    otherUser = User.objects.get(username=otherUsername);

    messages = Message.objects.filter( (Q(sender=user) & Q(receiver=otherUser)) | (Q(sender=otherUser) & Q(receiver=user)))
    messages = sorted(messages, key=operator.attrgetter('timestamp'))

    template = loader.get_template('HCG/myMessagesAll.html')
    context = {
        'username': request.user.username,
        'otherUsername' : otherUser.username,
        'messages' : messages,
        'pk' : otherUser.id,
    }
    return HttpResponse(template.render(context, request))










