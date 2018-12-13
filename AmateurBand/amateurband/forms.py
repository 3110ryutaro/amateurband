from .models import Article
from django import forms


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'text')

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(ArticleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.auto_focus = True

    def save(self, commit=True):
        article_info = super(ArticleForm, self).save(commit=False)
        article_info.user = self._user
        if commit:
            article_info.save()
        return article_info

