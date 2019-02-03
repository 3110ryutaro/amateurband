from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import RecruitmentForm, SearchForm, RecruitmentCommentForm, SendingMessageForm
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django import forms
from .models import Recruitment, RecruitmentComment,ReceiveMessage
from django.views.generic import FormView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

AmateurUser = get_user_model()


class IndexView(View):
    def get(self, request):
        return render(request, 'amateurband/index.html')


class HomeView(View):
    def get(self, request):
        recruitments = Recruitment.objects.all().order_by('-created_at')
        print(recruitments)
        form = SearchForm()
        if request.GET.get('q'):
            recruitments = Recruitment.objects.filter(title__contains=request.GET.get('q'))

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
            return redirect('main:recruitment_list')
        else:
            form = RecruitmentForm
            return render(request, 'amateurband/recruitment.html', {'form': form})


class RecruitmentDetailView(View):
    def get(self, request, recruitment_id):
        recruitment = get_object_or_404(Recruitment, pk=recruitment_id)
        comments = RecruitmentComment.objects.all().order_by('-created_date')
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
        user_id = self.request.user.user_id
        user = AmateurUser.objects.get(user_id=user_id)
        recruitments = user.recruitment.all()
        receive_messages = user.receive_messages.all()
        context = {
            'user': user,
            'recruitments': recruitments,
            'receive_messages': receive_messages
        }
        return render(request, 'amateurband/mypage.html', context)


class ConfigProfileView(View):
    def get(self, request):
        user = self.request.user
        return render(request, 'amateurband/config_profile.html', {'user': user})


class MessageDetailView(View):
    def get(self, request, **kwargs):
        message = ReceiveMessage.objects.get(id=self.kwargs.get('message_id'))
        return render(request, 'amateurband/message_detail.html', {'message': message})


class RecruitmentListView(View):
    def get(self, request, *args, **kwargs):
        recruitment_list = Recruitment.objects.all().order_by('-updated_at')
        context = {
            'recruitment_list': recruitment_list
        }
        return render(request, 'amateurband/recruitment_list.html', context)


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
        recruitment = get_object_or_404(Recruitment, id=self.kwargs.get('recruitment_id'))
        receive_user = recruitment.user
        context['receive_user'] = receive_user
        return context

    def get_form_kwargs(self):
        kwargs = super(MessageView, self).get_form_kwargs()
        recruitment = get_object_or_404(Recruitment, id=self.kwargs.get('recruitment_id'))
        user = recruitment.user
        kwargs['sending_user'] = self.request.user
        kwargs['receive_user'] = user
        return kwargs

    def post(self, request, *args, **kwargs):
        recruitment = get_object_or_404(Recruitment, id=self.kwargs.get('recruitment_id'))
        receive_user = recruitment.user
        sending_user = request.user
        form = SendingMessageForm(request.POST,
                                  sending_user=sending_user,
                                  receive_user=receive_user)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            text = form.cleaned_data['text']
            _receive_user = ReceiveMessage.objects.create(user=receive_user,
                                                          sending_user=sending_user,
                                                          subject=subject,
                                                          text=text)
            _receive_user.save()
            form.save(commit=True)

            return redirect(reverse('main:recruitment_detail',
                                    kwargs={'recruitment_id': recruitment.id}))


