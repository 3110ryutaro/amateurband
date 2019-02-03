from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import RecruitmentForm, SearchForm, RecruitmentCommentForm, SendingMessageForm, ProfileForm
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django import forms
from .models import Recruitment, RecruitmentComment, Footprint
from django.views.generic import FormView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

AmateurUser = get_user_model()


class IndexView(View):
    def get(self, request):
        return render(request, 'amateurband/index.html')


class HomeView(View):
    def str2bool(self, s):
        if s == "初心者":
            return True
        elif s == "経験者":
            return False

    def searchPass(self, **kwargs):
        dict = {}
        for key, value in kwargs.items():
            if value != 'None':
                dict[key] = value
        return dict


    def get(self, request):
        recruitments = Recruitment.objects.all().order_by('-created_at')
        print(recruitments)
        form = SearchForm()
        if request.GET.get('q'):
            recruitments = Recruitment.objects.filter(title__contains=request.GET.get('q'))
        if request.GET.get('user_age'):
            print(request.user)
            user_age = request.GET.get('user_age')
            user_instrument = request.GET.get('user_instrument')
            user_amateur_level = request.GET.get('user_amateur_level')
            user_area = request.GET.get('user_area')
            recruitments = Recruitment.objects.filter(age=user_age,
                                                      instrument=user_instrument,
                                                      amateur_level=self.str2bool(user_amateur_level),
                                                      area__contains=user_area)

        context = {
            'recruitments': recruitments,
            'form': form,
        }
        return render(request, 'amateurband/home.html', context)


class RecruitmentCreateView(LoginRequiredMixin, FormView):
    form_class = RecruitmentForm
    template_name = 'amateurband/recruitment.html'
    success_url = reverse_lazy('main:index')

    def get_form_kwargs(self):
        kwargs = super(RecruitmentCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = RecruitmentForm(request.POST, user=request.user)

        if form.is_valid():
            form.save(commit=True)
            return redirect('main:home')
        else:
            form = RecruitmentForm
            return render(request, 'amateurband/recruitment.html', {'form': form})


class RecruitmentDetailView(View):
    def get(self, request, recruitment_id):
        recruitment = get_object_or_404(Recruitment, pk=recruitment_id)
        comments = recruitment.recruitment_comment.order_by('-created_date')
        context = {
            'recruitment': recruitment,
            'comments': comments
        }
        return render(request, 'amateurband/recruitment_detail.html', context)


class RecruitmentEditView(View):

    def get(self, request, *args, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=kwargs.get('recruitment_id'))
        form = RecruitmentForm(instance=recruitment, user=request.user)
        context = {
            'form': form,
            'recruitment': recruitment,
        }
        return render(request, 'amateurband/recruitment_edit.html', context)

    def post(self, request, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=kwargs.get('recruitment_id'))
        form = RecruitmentForm(request.POST, instance=recruitment, user=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('main:recruitment_detail', kwargs={'recruitment_id': recruitment.id}))


class RecruitmentCommentView(FormView):
    form_class = RecruitmentCommentForm
    template_name = 'amateurband/recruitment_comment.html'
    success_url = reverse_lazy('main:home')

    def get_form_kwargs(self):
        kwargs = super(RecruitmentCommentView, self).get_form_kwargs()
        kwargs['recruitment'] = Recruitment.objects.get(id=self.kwargs['recruitment_id'])
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=kwargs.get('recruitment_id'))
        comment_user = request.user
        form = RecruitmentCommentForm(request.POST,
                                      recruitment=recruitment,
                                      user=comment_user)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('main:recruitment_detail',
                                    kwargs={'recruitment_id': recruitment.id}))


class MyPageView(View):
    def get(self, request, **kwargs):
        user = self.request.user
        receive_messages = user.receive_messages.filter(unread=False).order_by('-receiving_date')[:5]
        sending_messages = user.sending_messages.all()
        recruitments = user.recruitment.all().order_by('-updated_at')[:5]
        context = {
            'user': user,
            'recruitments': recruitments,
            'receive_messages': receive_messages,
            'sending_messages': sending_messages,
        }
        return render(request, 'amateurband/mypage.html', context)


class MyRecruitmentListView(View):
    def get(self, request):
        recruitment_list = request.user.recruitment.all()
        context = {
            'recruitment_list': recruitment_list
        }
        return render(request, 'amateurband/myrecruitment_list.html', context)


class MyMessageListView(View):
    def get(self, request):
        receive_messages = request.user.receive_messages.all()
        context = {
            'receive_messages': receive_messages
        }
        return render(request, 'amateurband/mymessage_list.html', context)


class MyProfileView(View):
    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, 'amateurband/myprofile.html', context)


class ConfigProfileView(FormView):
    form_class = ProfileForm
    template_name = 'amateurband/config_profile.html'

    def get_form_kwargs(self):
        kwargs = super(ConfigProfileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('main:show_profile')
        else:
            return render(request, 'amateurband/config_profile.html', {'form': form})


class EditProfileView(View):
    def get(self, request):
        user = request.user
        profile_info = user.profile
        form = ProfileForm(instance=profile_info, user=user)
        return render(request, 'amateurband/config_profile.html', {'form': form})

    def post(self, request, **kwargs):
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('main:show_profile')
        else:
            return render(request, 'amateurband/config_profile.html', {'form': form})


class MessageDetailView(View):
    def get(self, request, **kwargs):
        message_id = kwargs.get('message_id')
        user = self.request.user
        message = user.receive_messages.get(id=message_id)
        message.unread = True
        message.save()
        return render(request, 'amateurband/message_detail.html', {'message': message})


class RecruitmentDeleteView(View):
    def post(self, **kwargs):
        recruitment_id = kwargs.get('recruitment_id')
        recruitment = get_object_or_404(Recruitment, id=recruitment_id)
        recruitment.delete()
        return redirect('main:mypage')


class MessageView(FormView):
    form_class = SendingMessageForm
    template_name = 'amateurband/message.html'
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        receive_user = get_object_or_404(AmateurUser,
                                         username=self.kwargs.get('username'))
        context['receive_user'] = receive_user
        return context

    def get_form_kwargs(self):
        kwargs = super(MessageView, self).get_form_kwargs()
        receive_user = get_object_or_404(AmateurUser,
                                         username=self.kwargs.get('username'))
        kwargs['sending_user'] = self.request.user
        kwargs['receive_user'] = receive_user
        return kwargs

    def post(self, request, *args, **kwargs):
        receive_user = get_object_or_404(AmateurUser,
                                         username=kwargs.get('username'))
        sending_user = request.user
        form = SendingMessageForm(request.POST,
                                  sending_user=sending_user,
                                  receive_user=receive_user)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            _receive_user = receive_user.receive_messages.create(sending_user=sending_user,
                                                                 subject=subject,
                                                                 text=text)
            _receive_user.save()
            form.save(commit=True)

            return redirect(reverse('main:message',
                                    kwargs={'username': receive_user.username}))


class MessageReplyView(FormView):
    form_class = SendingMessageForm
    template_name = 'amateurband/message.html'
    success_url = reverse_lazy('main:home')

    def get_context_data(self, **kwargs):
        context = super(MessageReplyView, self).get_context_data(**kwargs)
        receive_user = AmateurUser.objects.get(username=self.kwargs.get('sending_username'))
        context['receive_user'] = receive_user
        return context

    def get_form_kwargs(self):
        kwargs = super(MessageReplyView, self).get_form_kwargs()
        receive_user = AmateurUser.objects.get(username=self.kwargs.get('sending_username'))
        kwargs['sending_user'] = self.request.user
        kwargs['receive_user'] = receive_user
        return kwargs

    def post(self, request, *args, **kwargs):
        receive_user = AmateurUser.objects.get(username=self.kwargs.get('sending_username'))
        sending_user = request.user
        form = SendingMessageForm(request.POST,
                                  sending_user=sending_user,
                                  receive_user=receive_user)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            _receive_user = receive_user.receive_messages.create(sending_user=sending_user,
                                                                 subject=subject,
                                                                 text=text)
            _receive_user.save()
            form.save(commit=True)

            return redirect(reverse('main:message_reply',
                            kwargs={'sending_username': receive_user.username}))


class UserDetailView(View):
    def get(self, request, **kwargs):
        username = kwargs.get('username')
        user = get_object_or_404(AmateurUser, username=username)
        if request.user.username == username:
            return render(request, 'amateurband/user_detail.html', {'user': user})
        if Footprint.objects.filter(user=request.user):
            request.user.footprint.footprint_user.add(user)
            return render(request, 'amateurband/user_detail.html', {'user': user})
        else:
            Footprint.objects.create(user=request.user)
            request.user.footprint.footprint_user.add(user)
            return render(request, 'amateurband/user_detail.html', {'user': user})


class FootPrintView(View):
    def get(self, request):
        footprint_users = request.user.footprints_user.all()
        context = {
            'footprint_users': footprint_users,
        }
        return render(request, 'amateurband/myfootprint.html', context)
