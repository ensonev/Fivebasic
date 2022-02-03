import email
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .serializers import UserRegister,UserData
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import update_last_login

@api_view(['GET'])
def apioverview(request):
    api_urls ={
   
        'registration':'/register',
        'update registered data':'register/<int:pk>'
    }
    return Response(api_urls)

class register(APIView):
    def get(self, request, format=None):
        userlist = User.objects.all()
        serializer = UserData(userlist,many=True)
        return Response(serializer.data, status=200)
    def post(self,request,format=None):      
        serializer=UserRegister(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']='registered'
            data['username']=account.username
            data['first_name']=account.first_name
            data['last_name']=account.last_name
            data['email']=account.email
            token,create=Token.objects.get_or_create(user=account)
            data['token']=token.key
        else:
            data=serializer.errors
        return Response(data, status=status.HTTP_200_OK)

class userDetails(generics.UpdateAPIView):
    serializer_class = UserData
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except:
            raise Http404
        
    def get(self,request,pk,format=None):
        userdata=self.get_object(pk)
        serializer=UserData(userdata)
        return Response(serializer.data)
    def update(self,request,pk,format=None,*args, **kwargs):
        userdata=self.get_object(pk)
        serializer=UserData(userdata,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error','error':serializer.errors})
    def delete(self,request,pk,format=None):
        userdata=self.get_object(pk)
        userdata.delete()
        return Response({'message':"user deleted"})

class loginToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result    