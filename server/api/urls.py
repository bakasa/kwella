from rest_framework.routers import DefaultRouter
from django.urls import path

from users.views import SignUpView

# non-viewsets
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
