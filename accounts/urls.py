from django.urls import path
from .views import SignupView, LoginView, logoutview

urlpatterns = [
    path('login/', LoginView.as_view(), name='login' ),
    path('signup/', SignupView.as_view(), name='signup' ),
    path('logout/', logoutview, name='logout' ),
]