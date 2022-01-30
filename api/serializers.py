from rest_framework import serializers
from .models import Task
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields ='__all__'

def c(*args, **kwargs):
	print(args)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # c(first_name)
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['roles'] = "superuser" if user.is_superuser else "normal_user"
        return token
