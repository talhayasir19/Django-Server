from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    logout,
    user_profile,
    verify_user
    )


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', logout),
    path('verify/<str:token>', verify_user),
    path('userDetail', user_profile),
    
]
