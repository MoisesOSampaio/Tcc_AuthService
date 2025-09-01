from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name','email', 'password','lideranca','cargo']
        read_only_fields = ['id']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        
        token['role'] = user.cargo


        return token