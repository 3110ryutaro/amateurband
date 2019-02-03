from .models import AmateurUser
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UsernameField


class SignUpForm(forms.ModelForm):
    class Meta:
        model = AmateurUser
        fields = ('username', 'email', 'password',)

    confirm_password = forms.CharField(
        label='confirm-password',
        required=True,
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

    def clean_username(self):
        """usernameのバリデーション"""
        username = self.cleaned_data['username']
        if AmateurUser.objects.filter(username=username):
            raise forms.ValidationError('この名前のユーザーは既に存在しています。')
        # usernameは3文字以上にならねばエラー表示。
        if len(username) < 3:
            raise forms.ValidationError('3文字以上のユーザー名にしてください。')
        # usernameがアルファベットを含んでなければエラー表示。
        if not username.isalpha():
            raise forms.ValidationError('半角アルファベットを用いてください')
        # usernameが数字だけであればエラー表示。
        if username.isnumeric():
            raise forms.ValidationError('数字と半角アルファベットを用いてください')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise forms.ValidationError('4文字以上のパスワードを入力してください')
        return password

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']

        if password != password2:
            raise forms.ValidationError('パスワードと確認用パスワードが合致していません')

    def save(self, commit=True):
        """passwordをハッシュ化してからユーザー情報の保存"""
        user_info = super(SignUpForm, self).save(commit=False)
        user_info.set_password(self.cleaned_data['password'])

        if commit:
            user_info.save()

        return user_info


class LoginForm(forms.Form):
    """ログインフォーム"""
    username = UsernameField(
        label='username',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Username',
                                      'autofocus': True})
    )
    password = forms.CharField(
        label='password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}, render_value=True)
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user_request_to_login = None
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_username(self):
        """Validation for username"""
        username = self.cleaned_data['username']
        return username

    def clean_password(self):
        """Validation for password"""
        password = self.cleaned_data['password']
        return password

    def clean(self):
        """Validation username corresponding to its password that was saved in Sign-Up."""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        try:
            requesting_user = AmateurUser.objects.get(username=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError('ユーザー名が間違っています ')
        if not requesting_user.check_password(password):
            raise forms.ValidationError('パスワードが間違っています')
        self.user_request_to_login = requesting_user

    def get_login_user(self):
        """ユーザ名、データベースIDなどを表す引数 user_id をとり、対応するUserオブジェクトを返す。"""
        return self.user_request_to_login
