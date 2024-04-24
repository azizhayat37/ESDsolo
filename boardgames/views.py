from django.shortcuts import render
from django.db.models import F
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import BoardGame
from .forms import LoginForm

# Create your views here.

# NEED TO CREATE A REGISTRATION PAGE
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'boardgames/register.html', {'form': form})
    

# NEED TO CREATE A LOGIN PAGE
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'boardgames/login.html', {'form': form})
    
def index(request):
    context = {}
    return render(request, 'boardgames/index.html', context)


def display(request, category=None):

    # in case of a GET request via the search bar (see base.html)
    category = request.GET.get('category', category)

    # return the correct category of games
    if category == None or category == 'all':
        games = BoardGame.objects.all()
    elif category == 'thematic':
        games = BoardGame.objects.filter(cat_thematic=True)
    elif category == 'strategy':
        games = BoardGame.objects.filter(cat_strategy=True)
    elif category == 'war':
        games = BoardGame.objects.filter(cat_war=True)
    elif category == 'family':
        games = BoardGame.objects.filter(cat_family=True)
    elif category == 'cgs':
        games = BoardGame.objects.filter(cat_cgs=True)
    elif category == 'abstract':
        games = BoardGame.objects.filter(cat_abstract=True)
    elif category == 'party':
        games = BoardGame.objects.filter(cat_party=True)
    elif category == 'childrens':
        games = BoardGame.objects.filter(cat_childrens=True)
    else:
        # if something passes in through search for something that isn't a category
        # search boardgames in the database by name
        games = BoardGame.objects.filter(name__icontains=category)

    # establish pagination 
    page = request.GET.get('page', 1)

    start = 1
    end = 21

    paginator = Paginator(games, end)
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)    
    
    context = { 
        'games': games,
        'range': range(start, end + 1),
        'pagination_range': f"{start},{end}",
    }
    return render(request, 'boardgames/display.html', context)