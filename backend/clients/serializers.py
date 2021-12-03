from django.contrib.auth import authenticate
from rest_framework import serializers

from .filelds import Base64ImageField
from .models import User


class CustomUserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()
    sex = serializers.ChoiceField(choices=[0, 1])
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(min_length=5)
    password = serializers.CharField(max_length=128, min_length=1)

    class Meta:
        fields = ('avatar', 'sex', 'first_name', 'last_name', 'email', 'password')
        model = User

    def validate_email(self, data):
        print(data)
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                'Email уже занят')
        return data

    
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Email уже занят')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
