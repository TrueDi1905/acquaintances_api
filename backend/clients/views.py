from rest_framework.authtoken.views import ObtainAuthToken

from .models import User
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from .serializers import CustomUserSerializer, CustomAuthTokenSerializer

from rest_framework import mixins


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        password = serializer.data['password']
        email = serializer.data['email']
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        serializer = CustomUserSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
