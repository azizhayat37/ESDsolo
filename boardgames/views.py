from django.shortcuts import render
from django.db.models import F
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
            return redirect('boardgames:index')
    else:
        form = UserCreationForm()
    return render(request, 'boardgames/register.html', {'form': form})
    

# NEED TO CREATE A LOGIN PAGE
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('boardgames:index')
            return redirect('boardgames:index')
    else:
        form = AuthenticationForm()
    return render(request, 'boardgames/login.html', {'form': form})
    


def index(request):
    context = {}
    return render(request, 'boardgames/index.html', context)