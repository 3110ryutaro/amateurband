from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': form})
        user_info_save = form.save(commit=True)
        auth_login(request, user_info_save)
        return redirect('main:profile')


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

        user_id = login_user.user_id

        return redirect(reverse('main:mypage', kwargs={'user_id': user_id}))


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

        return redirect(reverse('accounts:login'))