from .models import Recruitment, RecruitmentComment, SendingMessage
from django import forms


class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = ('title', 'instrument', 'amateur_level',
                  'age', 'area', 'comment')

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(RecruitmentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        article_info = super(RecruitmentForm, self).save(commit=False)
        article_info.user = self._user
        if commit:
            article_info.save()
        return article_info


class SearchForm(forms.Form):
    q = forms.CharField(max_length=150, label='キーワード')


class RecruitmentCommentForm(forms.ModelForm):
    class Meta:
        model = RecruitmentComment
        fields = ['name', 'text']

    def __init__(self, *args, **kwargs):
        self._recruitment = kwargs.pop('recruitment')
        self._user = kwargs.pop('user')
        super(RecruitmentCommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['value'] = self._user.username
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.auto_focus = True

    def save(self, commit=True):
        comment_info = super(RecruitmentCommentForm, self).save(commit=False)
        comment_info.recruitment = self._recruitment
        comment_info.user = self._user
        if commit:
            comment_info.save()
        return comment_info


class SendingMessageForm(forms.ModelForm):
    class Meta:
        model = SendingMessage
        fields = ['subject', 'text']

    def __init__(self, *args, **kwargs):
        self._sending_user = kwargs.pop('sending_user')
        self._receive_user = kwargs.pop('receive_user')
        super(SendingMessageForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        message_info = super(SendingMessageForm, self).save(commit=False)
        message_info.user = self._sending_user
        message_info.receive_user = self._receive_user
        if commit:
            message_info.save()
        return message_info


