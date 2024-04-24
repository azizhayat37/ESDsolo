from django.urls import path
from . import views

# made sure display path will work with or without a category parameter passed to it

urlpatterns = [
    path('', views.index, name='index'),
    path('login_veiw/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('display/', views.display, name='display'),
    path('display/<str:category>/', views.display, name='display'),
    path('logout_view/', views.logout_view, name='logout_view'),
]