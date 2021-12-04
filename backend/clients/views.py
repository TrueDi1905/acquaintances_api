from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Like, User
from .serializers import (CustomAuthTokenSerializer,
                          CustomUserGetSerializer,
                          CustomUserSerializer)
from .systems import add_watermark, calc_dist, send


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
        add_watermark(user.avatar)
        user.save()
        serializer = CustomUserGetSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer


class MatchViewSet(mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        client = request.user
        like_client = get_object_or_404(
            User, id=self.kwargs.get('client_id'))
        if like_client == client:
            return Response({'error': 'Нельзя лайкнуть самого себя'})
        if Like.objects.filter(client=client,
                               client_like=like_client).exists():
            return Response({
                'errors': 'Вы уже лайкали данного пользователя!'
            }, status=status.HTTP_400_BAD_REQUEST)
        like = Like(client=client, client_like=like_client)
        like.save()
        if Like.objects.filter(client=like_client,
                               client_like=client).exists():
            send(client, like_client)
            send(like_client, client)
        return Response({'Like': 'Лайк успешно отправлен'}, status=status.HTTP_201_CREATED)


class ListViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('first_name', 'last_name', 'sex')

    def get_queryset(self):
        if self.request.query_params.get('distance'):
            distance = self.request.query_params.get('distance')
            users = []
            for client in self.queryset:
                if calc_dist(client.lat, client.lon, self.request.user.lat,
                             self.request.user.lon) == int(distance):
                    users.append(client)
            return self.queryset.filter(email__in=users)
        return self.queryset
