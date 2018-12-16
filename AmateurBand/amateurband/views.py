from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from .forms import ArticleForm
from django.urls import reverse_lazy
from .models import Article
from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

AmateurUser = get_user_model()


class IndexView(View):
    def get(self, request):
        article_list = Article.objects.all()
        context = {
            'article_list': article_list
    }
        return render(request, 'amateurband/index.html', context)


class ArticleView(LoginRequiredMixin, FormView):
    form_class = ArticleForm
    template_name = 'amateurband/article.html'
    success_url = reverse_lazy('main:index')

    def get_form_kwargs(self):
        kwargs = super(ArticleView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request):

        form = ArticleForm(request.POST, user=request.user)

        if form.is_valid():
            form.save(commit=True)
            return redirect('main:index')
        else:
            form = ArticleForm
            return render(request, 'amateurband/article.html', {'form': form})


class MyPageView(View):
    def get(self, request, **kwargs):

        user_id = kwargs['user_id']
        user = AmateurUser.objects.get(user_id=user_id)
        context = {
            'mypage': user.username + 'のページです'
        }
        return render(request, 'amateurband/mypage.html', context)


class ArticleListView(View):
    def get(self, request):
        user = request.user
        article_list = user.articles.all()
        context = {
            'article_list': article_list
        }
        return render(request, 'amateurband/article_list.html', context)


class ArticleEditView(View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        form = ArticleForm(instance=article)
        context = {
            'form': form
        }
        return render(request, 'amateurband/article_edit.html', context)


class ArticleUpdateView(View):
    def get(self):
        pass


class ArticleDeleteView(View):
    def get(self):
        pass


class MessageView(View):
    def get(self, request):
        pass


class ProfileView(View):
    def get(self):
        pass

