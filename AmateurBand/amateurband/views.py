from django.shortcuts import render, redirect,reverse
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

        user = AmateurUser.objects.get(pk=request.user.user_id)
        form = ArticleForm(request.POST, user=user)

        if form.is_valid():
            form.save(commit=True)
            return redirect('main:index')
        else:
            form = ArticleForm
            return render(request, 'amateurband/article.html', {'form': form})


