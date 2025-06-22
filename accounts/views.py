from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView as DjangoLoginView



class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('home')



class LoginView(DjangoLoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    

def logoutview(request):
    logout(request)
    return redirect(reverse('home'))


    
    
