from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import RecruitmentForm, SearchForm, RecruitmentCommentForm, SendingMessageForm, ProfileForm
from django.urls import reverse_lazy
from .models import Recruitment, RecruitmentComment, Footprint, UserProfile, SearchWord
from django.db.models import Q
from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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

    def get(self, request):
        recruitments = Recruitment.objects.all().order_by('-created_at')
        print(recruitments)
        form = SearchForm()

        if request.GET.get('q'):
            recruitments = Recruitment.objects.filter(Q(title__contains=request.GET.get('q')) |
                                                      Q(instrument__contains=request.GET.get('q')) |
                                                      Q(area__contains=self.return_str(request.GET.get('q'))) |
                                                      Q(comment__contains=request.GET.get('q')))
            if not request.user.searchwords.filter(word=request.GET.get('q')).exists():
                request.user.searchwords.create(user=request.user, word=request.GET.get('q'))

        if request.GET.get('user_age'):
            user_age = request.GET.get('user_age')
            user_gender = request.GET.get('user_gender')
            user_instrument = request.GET.get('user_instrument')
            user_amateur_level = request.GET.get('user_amateur_level')
            user_area = request.GET.get('user_area')
            recruitments = Recruitment.objects.filter(Q(gender=user_gender) | Q(gender=3),
                                                      age=user_age,
                                                      instrument=user_instrument,
                                                      amateur_level=self.str2bool(user_amateur_level),
                                                      area__contains=self.return_str(user_area))

            print(recruitments)
        profile_none_users = UserProfile.objects.filter(Q(age__isnull=True) |
                                                        Q(instrument__isnull=True) |
                                                        Q(amateur_level__isnull=True) |
                                                        Q(area__isnull=True))
        user = None
        for none_user in profile_none_users:
            if none_user.user.user_id == request.user.user_id:
                user = none_user

        context = {
            'recruitments': recruitments,
            'form': form,
            'profile_none_user': user
        }
        return render(request, 'amateurband/home.html', context)

    def return_str(self, s):
        return s[0:2]


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
            messages.info(request, "募集記事を投稿しました。")
            return redirect('main:home')
        else:
            form = RecruitmentForm
            return render(request, 'amateurband/recruitment.html', {'form': form})


class RecruitEditView(View):
    def get(self, request, *args, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=self.kwargs.get('recruitment_id'))
        form = RecruitmentForm(instance=recruitment, user=request.user)
        context = {
            'form': form,
            'recruitment': recruitment,
        }
        return render(request, 'amateurband/recruitment_edit.html', context)

    def post(self, request, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=self.kwargs.get('recruitment_id'))
        form = RecruitmentForm(request.POST, instance=recruitment, user=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('main:recruitment_detail', kwargs={'recruitment_id': recruitment.id,
                                                                       'username': recruitment.user.username}))


class RecruitmentDetailView(View):
    def get(self, request, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=kwargs.get('recruitment_id'))
        recruitment_user = get_object_or_404(AmateurUser, username=kwargs.get('username'))
        recruitments = recruitment_user.recruitment.all().order_by('-updated_at')
        comments = recruitment.recruitment_comment.order_by('-created_date')
        context = {
            'recruitment': recruitment,
            'recruitments': recruitments,
            'comments': comments,
        }
        if Footprint.objects.filter(user=request.user):
            request.user.footprint.footprint_user.add(recruitment_user)
        else:
            Footprint.objects.create(user=request.user)
            request.user.footprint.footprint_user.add(recruitment_user)

        return render(request, 'amateurband/recruitment_detail.html', context)


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
                                    kwargs={'recruitment_id': recruitment.id,
                                            'username': recruitment.user.username}))


class RecruitmentDeleteView(View):
    def post(self, request, **kwargs):
        recruitment = get_object_or_404(Recruitment, pk=kwargs.get('recruitment_id'))
        recruitment.delete()
        messages.warning(request, "募集記事を削除しました。")
        return redirect('main:recruitment_list')


class MyPageView(View):
    def get(self, request, **kwargs):
        user = self.request.user
        print(user)
        receive_messages = user.receive_messages.filter(unread=False).order_by('-receiving_date')[:3]
        sending_messages = user.sending_messages.all()
        recruitments = user.recruitment.all().order_by('-updated_at')[:5]
        query_set = []
        context = {}
        if user.kind == 1:
            context = {
                'user': user,
                'recruitments': recruitments,
                'receive_messages': receive_messages,
                'sending_messages': sending_messages,
            }
        if user.kind == 2:
            words = user.searchwords.all()
            print(words)
            for w in words:
                q1 = Recruitment.objects.filter()
                q2 = q1.filter(Q(title__contains=w.word) |
                               Q(instrument__contains=w.word) |
                               Q(area__contains=w.word) |
                               Q(comment__contains=w.word))
                for q in q2:
                    if q not in query_set:
                        query_set.append(q)

            context = {
                'user': user,
                'recruitments': recruitments,
                'receive_messages': receive_messages,
                'sending_messages': sending_messages,
                'query_set': self.returnQuerySet(query_set),
                'page': self.querySetCount(query_set),
                'page_active': int(request.GET.get('page')),
                'page_last': 5,
            }
        return render(request, 'amateurband/mypage.html', context)

    def querySetCount(self, *args):
        page_count = 0
        if int(len(*args)) % 5 == 0:
            page_count = int(len(*args) / 5)
            return range(1, page_count + 1)

        page_count = int(len(*args) / 5)
        return range(1, page_count + 2)

    def returnQuerySet(self, args):
        query_set = []
        page = self.request.GET.get('page')
        if page == "1":
            query_set = args[0:5]
        elif page == "2":
            query_set = args[5:10]
        elif page == "3":
            query_set = args[10:15]
        elif page == "4":
            query_set = args[15:20]
        elif page == "5":
            query_set = args[20:25]
        elif page == "6":
            query_set = args[25:30]
        elif page == "7":
            query_set = args[30:35]
        elif page == "8":
            query_set = args[35:40]
        elif page == "9":
            query_set = args[40:45]
        elif page == "10":
            query_set = args[45:50]
        return query_set

    def post(self, request):
        if request.POST.get('comment_id'):
            comment = get_object_or_404(RecruitmentComment, pk=request.POST.get('comment_id'))
            comment.admission = True
            comment.save()
        return redirect('main:mypage')


class MyRecruitmentListView(View):
    def get(self, request):
        recruitment_list = request.user.recruitment.all().order_by('-updated_at')
        context = {
            'recruitment_list': recruitment_list
        }
        return render(request, 'amateurband/myrecruitment_list.html', context)


class MyMessageListView(View):
    def get(self, request):
        users = []
        receive_messages = request.user.receive_messages.all().order_by('-receiving_date')
        sending_messages = request.user.sending_messages.all().order_by('-sending_date')
        user_list = request.user.receive_messages.values_list('sending_user__username', flat=True).distinct()
        for user in user_list:
            users.append(get_user_model().objects.get(username=user))
        for user in users:
            print(user)
        print(AmateurUser.objects.get(user_id=1))
        context = {
            'receive_messages': receive_messages,
            'sending_messages': sending_messages,
            'user_list': users
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
            messages.success(request, "プロフィールを作成しました。")
            return redirect('main:show_profile')
        else:
            messages.error(request, "エラーにより作成できませんでした。")
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
            messages.success(request, "プロフィールを更新しました。")
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
            messages.success(request, "メッセージの送信が完了しました。")
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
            messages.success(request, "メッセージの送信が完了しました。")
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
