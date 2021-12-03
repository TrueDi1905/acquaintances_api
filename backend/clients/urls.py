from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register('create', views.UserViewSet, basename='create')
router.register(r'(?P<client_id>[\d]+)/match', views.MatchViewSet, basename='match')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.CustomObtainAuthToken.as_view(), name='auth'),

]
