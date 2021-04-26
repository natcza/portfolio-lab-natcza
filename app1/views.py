from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse
from .models import Donation, Institution, Category
from .forms import RegisterUserForm, LoginUserForm
# Create your views here.

User = get_user_model()

class LandingPageView(View):
    template_name = 'app1/index.html'

    def get(self, request, *args, **kwargs):

        donations = Donation.objects.all()
        count_quantity = 0
        count_institution = 0

        for donation in donations:
            count_quantity += donation.quantity

            # ile jest wspartych instytucji? - nie istotnie czy różnych czy tych samych
            count_institution += 1

        #  Dynamiczne ładowanie instytucji
        institutions = Institution.objects.filter(type=1)
        list_institutons = []

        for institution in institutions:

            name = institution.name
            description = institution.description
            category = ''
            institution_get = Institution.objects.get(pk=institution.pk)

            for _ in institution_get.categories.all():
                category += str(_) + ', '

            category = category[0: len(category)-2]
            list_institutons.append({'name': name, 'description': description, 'category': category})

        # breakpoint()
        organisations = Institution.objects.filter(type=2)
        list_organisations = []
        for organisation in organisations:

            name = organisation.name
            description = organisation.description
            category = ''
            organisation_get = Institution.objects.get(pk=organisation.pk)

            for _ in organisation_get.categories.all():
                category += str(_) + ', '

            category = category[0: len(category) - 2]
            list_organisations.append({'name': name, 'description': description, 'category': category})

        local_organisations = Institution.objects.filter(type=3)
        list_local_organisations = []
        for local_organisation in local_organisations:

            name = local_organisation.name
            description = local_organisation.description
            category = ''
            local_organisation_get = Institution.objects.get(pk=local_organisation.pk)

            for _ in local_organisation_get.categories.all():
                category += str(_) + ', '

            category = category[0: len(category) - 2]
            list_local_organisations.append({'name': name, 'description': description, 'category': category})

        ctx = {
            'count_quantity': count_quantity,
            'count_institution': count_institution,
            'list_institutons': list_institutons,
            'list_organisations': list_organisations,
            'list_local_organisations': list_local_organisations,
        }
        return render(request, self.template_name, ctx)


class AddDonationView(View):
    template_name = 'app1/form.html'


    # breakpoint()
    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        institutions = Institution.objects.all()
        # institutions_categories = Institution.objects.order_by(categories)

        ctx = {
            'categories': categories,
            'institutions': institutions,
            # 'inst_cats': istitutions_c,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        institution = request.POST.get('organization')
        #wyjac z requesta talice idkow categorii

        #pobrac z bazy kategorie o tych idkach
        post_data = {
            'quantity': request.POST.get('bags'),
            'institution': Institution.objects.get(pk=institution),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('postcode'),
            'phone_number': request.POST.get('phone'),
            # 'pick_up_date': request.POST.get('data'),
            # 'pick_up_time': request.POST.get('time'),
            'pick_up_date': '2020-03-11',
            'pick_up_time': '12:00:00',
            'pick_up_comment': request.POST.get('more_info'),
            'user': request.user
        }
        donation = Donation.objects.create(**post_data)

        categoriesIds = request.POST.getlist('categories')
        # breakpoint()
        for id in categoriesIds:
            category = Category.objects.get(pk=id)
            donation.categories.add(category)
        # return redirect('confirmation')
        return JsonResponse({'url': reverse('add-donation')})

class LoginView(View):
    form_class = LoginUserForm
    template_name = 'app1/login.html'

    def get(self, request, *args, **kwargs):
        ctx = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        message = None

        if form.is_valid():
            # jeśli jest True, to zaloguj użytkownika
            # breakpoint()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # dla django 2.2
            # user = authenticate(username, password)
            # dla django 3.x
            user = authenticate(email=email, password=password)
            if user:
                # login user
                login(request, user)
                return redirect('landing-page')
            else:
                # not login

                message = 'Podaj poprawne dane'
                return redirect('register')


        else:
            # jeśli False, to wyświetl komunikat
            message = "Uzupełnij poprawnie dane"


        context = {
            'form': form,
            'message': message,
        }
        return render(request, self.template_name, context)

class LogoutView(View):
    # form_class = LoginUserForm
    template_name = 'app1/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            # ctx = {}
            return redirect('landing-page')
        # return render(request, self.template_name, ctx)

class RegisterView(View):
    form_class = RegisterUserForm
    template_name = 'app1/register.html'

    def get(self, request, *args, **kwargs):

        ctx = {
            'form': self.form_class(),

        }
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # zapisz dane użytkownika
            User.objects.create_user(
                email=cd['email'],
                password=cd['password'],  # make_password
                first_name=cd['name'],
                last_name=cd['surname']
            )


            return redirect('login')
        ctx = {

            }
        return render(request, self.template_name, ctx)

class UserView(LoginRequiredMixin, View):
    template_name = 'app1/user.html'

    def get(self, request, *args, **kwargs):

        ctx = {}
        return render(request, self.template_name, ctx)

class ConfirmationView(LoginRequiredMixin, View):
    template_name = 'app1/form-confirmation.html'

    def get(self, request, *args, **kwargs):

        ctx = {}
        return render(request, self.template_name, ctx)