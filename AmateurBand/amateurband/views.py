from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import RecruitmentForm, ProfileForm
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django import forms
from .models import Recruitment
from django.views.generic import FormView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

AmateurUser = get_user_model()


class IndexView(View):
    def get(self, request):
        return render(request, 'amateurband/index.html')


class RecruitmentView(LoginRequiredMixin, FormView):
    form_class = RecruitmentForm
    template_name = 'amateurband/recruitment.html'
    success_url = reverse_lazy('main:index')

    def get_form_kwargs(self):
        kwargs = super(RecruitmentView, self).get_form_kwargs()
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


class EntryView(LoginRequiredMixin, View):
    def get(self):
        pass

# class ArticleView(LoginRequiredMixin, FormView):
#     form_class = ArticleForm
#     template_name = 'amateurband/article.html'
#     success_url = reverse_lazy('main:index')
#
#     def get_form_kwargs(self):
#         kwargs = super(ArticleView, self).get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
#
#     def post(self, request):
#
#         form = ArticleForm(request.POST, user=request.user)
#
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect('main:index')
#         else:
#             form = ArticleForm
#             return render(request, 'amateurband/article.html', {'form': form})


class ProfileView(View):
    def get(self, request, **kwargs):
        user_id = kwargs['user_id']
        return render(request, 'amateurband/profile.html', {'user_id': user_id})


class MyPageView(View):
    def get(self, request, **kwargs):
        user_id = self.request.user.user_id
        user = AmateurUser.objects.get(user_id=user_id)
        recruitments = user.recruitment.all()
        context = {
            'user': user,
            'recruitments': recruitments
        }
        return render(request, 'amateurband/mypage.html', context)


class RecruitmentListView(View):
    def get(self, request, *args, **kwargs):
        recruitment_list = Recruitment.objects.all().order_by('-updated_at')
        context = {
            'recruitment_list': recruitment_list
        }
        return render(request, 'amateurband/recruitment_list.html', context)


class RecruitmentDetailView(View):
    def get(self, request, recruitment_id):
        recruitment = get_object_or_404(Recruitment, pk=recruitment_id)
        context = {
            'recruitment': recruitment
        }
        return render(request, 'amateurband/recruitment_detail.html', context)


# class ArticleEditView(View, FormMixin):
#
#     def get(self, request, article_id):
#         article = get_object_or_404(Article, pk=article_id)
#         form = ArticleUpdateForm(instance=article)
#         context = {
#             'form': form,
#             'article': article,
#         }
#         return render(request, 'amateurband/article_edit.html', context)
#
#     def post(self, request, article_id):
#         # article = get_object_or_404(Article, pk=article_id)
#         form = ArticleUpdateForm(request.POST, user=request.user)
#         if form.is_valid():
#             form.save(commit=True)
#             return redirect('main:article_list')
#
#
# class ArticleDeleteView(View):
#     def get(self):
#         pass


class MessageView(View):
    def get(self, request):
        pass


