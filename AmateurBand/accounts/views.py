from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView

from .forms import SignUpForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class RecruitEntryChoiceView(View):
    def get(self, request):
        return render(request, 'accounts/recruit_entry.html')


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
        kwargs['kind'] = self.kwargs.get('kind')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['kind'] = self.kwargs.get('kind')
        return context

    def post(self, request, **kwargs):
        form = SignUpForm(request.POST, kind=kwargs.get('kind'))
        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': form})
        user_info_save = form.save(commit=True)
        print(user_info_save)
        auth_login(request, user_info_save)

        return redirect('main:config_profile')


class LoginView(View):
    """ログインページ"""
    def get(self, request, **kwargs):
        loginform = LoginForm

        context = {
            'loginform': loginform,
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        context = {'loginform': form}

        if not form.is_valid():
                        return render(request, 'accounts/login.html', context)

        login_user = form.get_login_user()
        auth_login(request, login_user)

        return redirect('main:mypage')


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

        return redirect(reverse('main:index'))

