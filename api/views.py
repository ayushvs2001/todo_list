from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from .forms import UserRegistrationForm
from .serializers import TaskSerializer, CustomTokenObtainPairSerializer
from .models import Task
from .custom_permission import MyPermission

from rest_framework import exceptions, status, views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import  (IsAuthenticated, IsAdminUser, AllowAny)
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

######### Todo Controller ###########

@login_required(login_url='login')
def list(request):
	return render(request, 'api/todo_list.html')


def unauthorized(request):
	return HttpResponse('401 Unauthorized Error', status=401)


# Todo Controller
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class TaskLC(ListCreateAPIView):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyPermission]


class TaskRUD(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


############## AuthController #############
def user_registration(request):
     if not request.user.is_authenticated:
         form = UserRegistrationForm()
         if request.method == "POST":
             form = UserRegistrationForm(request.POST)

             if form.is_valid():
                 user = form.save()
                 username = form.cleaned_data.get('username')
                 messages.success(request, f"user register successfully  + {username}")

                 return redirect('login')
             else:
                 print("error")
         return render(request, 'api/register.html', context={'form': form})

     else:
        logout(request)
        return redirect('login')

def user_login(request):
   if not request.user.is_authenticated:
      if request.method == 'POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request, username=username, password=password)

         if user:
             login(request, user)
             return redirect("home")
         else:
             messages.info(request, "username or password is invalid")

      return render(request, 'api/login_form.html', context={})
   else:
      logout(request)
      return redirect('login')


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')
