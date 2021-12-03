from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register('', views.UserViewSet, basename='create')

urlpatterns = [path('create/', include(router.urls)),
               path('auth/', views.CustomObtainAuthToken.as_view(), name='auth')
]
