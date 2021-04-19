from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password

# Import modeli do widoku
from .models import Category, Institution, Donation


# from accounts.forms import RegisterForm, LoginForm


class LandingPageView(View):
    template_name = 'app1/index.html'

    def get(self, request, *args, **kwargs):
        """Pobranie informacji o datkach"""
        donations = Donation.objects.all()
        quantity_of_bags = 0
        quantity_of_institution = 0

        for donation in donations:
            quantity_of_bags = quantity_of_bags + donation.quantity  #donation.quantity (model Donation, pole quantity)
            quantity_of_institution = quantity_of_institution + 1
        # breakpoint()
        ctx = {
            'quantity_of_bags': quantity_of_bags,
            'quantity_of_institution': quantity_of_institution,
        }
        return render(request, self.template_name, ctx)


class AddDonationView(View):
    template_name = 'app1/form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(View):
    template_name = 'app1/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = 'app1/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
