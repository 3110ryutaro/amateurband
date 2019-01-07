from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(View):
    def get(self, request, signup_id):

        context = {
            'form': SignUpForm
        }
        if signup_id == 1:
            return render(request, 'accounts/recruit_signup.html', context)
        elif signup_id == 2:
            return render(request, 'accounts/entry_signup.html', context)

    def post(self, request, signup_id):
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/recruit_signup.html', {'form': form})
        user_info_save = form.save(commit=True)
        auth_login(request, user_info_save)
        if signup_id == 1:
            return redirect('main:new_recruitment')
        elif signup_id == 2:
            return redirect('main:recruit_list')


class LoginView(View):
    """ログインページ"""
    def get(self, request, *args, **kwargs):
        form = LoginForm
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/login.html', {'form': form})

        login_user = form.get_login_user()
        auth_login(request, login_user)

        return redirect(reverse('main:index'))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

        return redirect(reverse('accounts:login'))