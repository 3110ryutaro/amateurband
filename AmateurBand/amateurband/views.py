from django.shortcuts import render, redirect,reverse
from django.views import View
from .forms import ArticleForm
from .models import Article
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

AmateurUser = settings.AUTH_USER_MODEL


class IndexView(View):
    def get(self, request):
        article_list = Article.objects.all()
        context = {
            'article_list': article_list
    }
        return render(request, 'amateurband/index.html', context)


class ArticleView(LoginRequiredMixin, View):
    def get(self, request):
        form = ArticleForm
        context = {
            'form': form
        }
        return render(request, 'amateurband/article.html', context)

    def post(self, request):
        form = ArticleForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('main:index')
        else:
            form = ArticleForm
            return render(request, 'amateurband/article.html', {'form': form})


