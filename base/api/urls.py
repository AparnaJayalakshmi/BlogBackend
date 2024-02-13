from django.urls import path
from . import views
from .views import BlogView,RegisterView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)
from .views import MyTokenObtainPairView

urlpatterns = [
    path('',views.getRoutes),
    path('register/',RegisterView.as_view()),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('blog/',BlogView.as_view())
]