from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, reverse, resolve_url
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import SignUpForm, LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from .models import AmateurUser
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView,
                                       PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import  send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import  BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.template.loader import get_template
from django.views import generic
from django.contrib import messages

User = get_user_model()


class RecruitEntryChoiceView(View):
    def get(self, request):
        return render(request, 'accounts/recruit_entry.html')


class SignUpView(generic.CreateView):
    """ユーザー仮登録"""
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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('accounts/mail_template/create/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('accounts/mail_template/create/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('accounts:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録画面"""
    template_name = 'accounts/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'accounts/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, *args, **kwargs):
        """tokenが正しければ本登録"""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録する
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)


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
        url = resolve_url('main:mypage')
        url += '?page=1'
        messages.info(request, "ログインしました。")
        return redirect(url)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)

        return redirect(reverse('main:index'))


class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'accounts/mail_template/password_reset/subject.txt'
    email_template_name = 'accounts/mail_template/password_reset/message.txt'
    template_name = 'accounts/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accounts/password_reset_complete.html'