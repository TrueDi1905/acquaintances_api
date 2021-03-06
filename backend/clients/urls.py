from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('create', views.UserViewSet, basename='create')
router.register(r'(?P<client_id>[\d]+)/match',
                views.MatchViewSet, basename='match')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.CustomObtainAuthToken.as_view(), name='auth'),
    path('list/', views.ListViewSet.as_view({'get': 'list'}), name='list')
]
