"""todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api import  views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
       ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
           path('admin/', admin.site.urls),

           ###### todo interface ######
           path("", views.list, name='home'),

           ###########  swagger interface for testing  ###########
           path('swag/', schema_view.with_ui('swagger', cache_timeout=0), name='swag'),

           ###########  unauthorized error page   ###########
           path('unauthorized/', views.unauthorized, name="unauthorized"),

           ###########  Todo controller  ###########
           path('api/', views.TaskLC.as_view(), name="api"),
           path('api/<pk>/', views.TaskRUD.as_view()),

           ###########  Token Authentication Controller  ###########
           path('gettoken/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
           path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
           path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),

           ########### sign in and sign up section #################
           path('accounts/login/', views.user_login, name='login'),
           path('accounts/logout/', views.user_logout, name='logout'),
           path('register/', views.user_registration, name='user_register'),

]
