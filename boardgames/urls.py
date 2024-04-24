from django.urls import path
from . import views

# made sure display path will work with or without a category parameter passed to it

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('display/', views.display, name='display'),
    path('display/<str:category>/', views.display, name='display'),
]