from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import LoginView, SignUpView
from trips.views import TripViewSet

app_name = 'api'

router = DefaultRouter()
router.register('trips', TripViewSet, basename='trips')

# non-viewsets views
urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'), #generates new access token for valid refresh token
    
]
