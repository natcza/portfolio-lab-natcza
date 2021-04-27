from django.contrib import admin
from django.urls import path

from app1.views import (
    LandingPageView,
    AddDonationView,
    LoginView,
    LogoutView,
    RegisterView,
    UserView,
    ConfirmationView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('add_donation/', AddDonationView.as_view(), name='add-donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name='user'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),


]