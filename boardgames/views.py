from django.shortcuts import render
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import BoardGame
from .forms import LoginForm, RegisterForm
from .cart import add_to_cart, return_user_cart, checkout


# Create your views here.

def index(request):
    context = {}
    return render(request, 'boardgames/index.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # Use the custom RegisterForm
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in
            return redirect('index')
    else:
        form = RegisterForm()  # Instantiate a blank version of your custom form
    return render(request, 'boardgames/register.html', {'form': form})
    

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'boardgames/login.html', {'form': form})


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

    if not games:
        #if there are no games that match the search, flash a warning and show all games
        messages.warning(request, 'No games found!')
        return redirect('display')

    # establish pagination, see tags.py under templatetags for more info
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


def cart_view(request):
    user_cart = return_user_cart(request)
    if user_cart is not None:
        total_price = 0 #REPLACE WITH REAL VALUE LATER
        for item in user_cart:
            total_price += item.quantity * item.boardgame.price
        context = {
            'user_cart': user_cart,
            'total_price': total_price
        }
        return render(request, 'boardgames/cart.html', context)
    else:
        messages.warning(request, "There's nothing in your cart!")
        return redirect('index')


def logout_view(request):
    auth_logout(request)
    return redirect('index')