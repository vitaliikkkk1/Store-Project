from typing import Any

from django import http
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginViews(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class  = UserLoginForm
    success_url = reverse_lazy('index')
    title = 'Store - авторизація'

class UserRegistrationView(TitleMixin, SuccessMessageMixin ,CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Ви успішно зареєструвалися'
    title = 'Store - реєстрація'




class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - особистий кабінет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))



class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - підтвердження електронної пошти'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email = kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
