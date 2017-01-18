from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from users.forms import UserRegistrationForm, LoginForm

# Create your views here.


def registration_view(request):
    context = dict()
    context['registration_form'] = UserRegistrationForm()
    context.update(csrf(request))
    if request.POST:
        form = UserRegistrationForm(request.POST)
        context['registration_form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            return HttpResponseRedirect('/')
        else:
            context['registration_form'] = form
    return render(request, "registration.html", context)


def login_view(request):
    context = dict()
    context['login_form'] = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled!")
            else:
                context['login_error'] = "User not found or incorrect information"
                return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

