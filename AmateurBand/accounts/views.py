from django.shortcuts import render, redirect, reverse
from .forms import SignUpForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class SignUpView(View):
    def get(self, request):

        context = {
            'form': SignUpForm()
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': form})
        user_info_save = form.save(commit=True)
        auth_login(request, user_info_save)

        return redirect('main:config_profile')


class LoginView(View):
    """ログインページ"""
    def get(self, request, **kwargs):
        signupform = SignUpForm
        loginform = LoginForm
        if kwargs.get('login_id') == 1:
            login_id = 1
        elif kwargs.get('login_id') == 2:
            login_id = 2
        elif kwargs.get('login_id') == 3:
            login_id = 3

        context = {
            'signupform': signupform,
            'loginform': loginform,
            'login_id': login_id,
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        context = {'loginform': form,
                   'signupform': SignUpForm,
                   'login_id': kwargs.get('login_id')}

        if not form.is_valid():
                        return render(request, 'accounts/login.html', context)

        login_user = form.get_login_user()
        auth_login(request, login_user)

        if kwargs.get('login_id') == 1:
            return redirect('main:new_recruitment')
        elif kwargs.get('login_id') == 2:
            return redirect('main:recruitment_list')
        elif kwargs.get('login_id') == 3:
            return redirect('main:index')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

        return redirect(reverse('main:index'))

