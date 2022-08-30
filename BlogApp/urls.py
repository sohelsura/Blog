from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('about', about, name="about"),
    path('blog', blog, name="blog"),
    path('blog-details/<int:id>', blogdetails, name="blogdetails"),
    path('contact', contact, name="contact"),
    path('team', team, name="team"),
    path('signup' ,signup, name="signup"),
    path('userlogin' ,userlogin, name="userlogin"),
    path('createblog', createblog, name="createblog"),
    path('logout', userlogout, name="logout")
]