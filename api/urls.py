from django.urls import path
from django.conf.urls import url
from .views import apioverview,register,userDetails,loginToken,userExistOrNot
urlpatterns = [
    path('',apioverview,name='apioverview'),
    path('register',register.as_view(),name='register'),
    path('register/<int:pk>',userDetails.as_view(),name='register'),
    path('login',loginToken.as_view(),name='login'),
    path('username-exist-or-not',userExistOrNot.as_view(),name='username-exist-or-not'),
]