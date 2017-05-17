from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from .models import Dish
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm,RegisterForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
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

        title = ''
        if request.GET.get('q','') != '':
            dishList = Dish.objects.filter(dishName__icontains = request.GET.get('q',''))
            title = 'Search Results'
        else:
            dishList = Dish.objects.filter(dishPublisher=request.user)
            title = 'Your Recipies'

        template = loader.get_template('HCG/homepageTemplate.html')
        context = {
            'dishList': dishList,
            'username': request.user.username,
            'title': title,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/HCG/loginPage')

def AllFoods(request):

    if request.user.is_authenticated:
        dishList = Dish.objects.filter(dishCategory='Food')
        template = loader.get_template('HCG/homepageTemplate.html')
        context = {
            'dishList': dishList,
            'username': request.user.username,
            'title': 'All Foods',
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/HCG/loginPage')

def AllDrinks(request):

    if request.user.is_authenticated:
        dishList = Dish.objects.filter(dishCategory='Drink')
        template = loader.get_template('HCG/alldrinksTemplate.html')
        context = {
            'dishList': dishList,
            'username': request.user.username,
            'title': 'All Drinks',
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

def DishFavourite(request):
    dishID = request.POST['dish'];
    dish = Dish.objects.get(id=dishID)
    dish.dishFavourited = True
    dish.save()
    return render(request,'dishListTemplate.html',{'dishList' : Dish.objects.all()})