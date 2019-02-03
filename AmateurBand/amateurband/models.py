from django.contrib.auth import get_user_model
from django.db import models

AmateurUser = get_user_model()

AGE_CHOICES = (
        (1, '10～20歳'),
        (2, '20～30歳'),
        (3, '30～40歳'),
        (4, '40～50歳'),
        (5, '50～60歳'),
        (6, '60～70歳'),
    )
INSTRUMENT_CHOICES = (
        ('ヴォーカル', 'ヴォーカル'),
        ('ギター', 'ギター'),
        ('ベース', 'ベース'),
        ('ドラム', 'ドラム'),
        ('キーボード', 'キーボード'),
        ('その他', 'その他'),
    )


class Recruitment(models.Model):

    user = models.ForeignKey(AmateurUser,
                             related_name='recruitment',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='タイトル')
    instrument = models.CharField(max_length=10,
                                  verbose_name='募集楽器',
                                  choices=INSTRUMENT_CHOICES,
                                  blank=True, null=True)
    amateur_level = models.BooleanField(default=False, verbose_name='初心者歓迎')
    age = models.IntegerField(verbose_name='年齢制限',
                              choices=AGE_CHOICES,
                              blank=True, null=True)
    area = models.CharField(verbose_name='活動地域', max_length=100, default='東京都')
    comment = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RecruitmentComment(models.Model):
    recruitment = models.ForeignKey(Recruitment,
                                    on_delete=models.CASCADE,
                                    related_name='recruitment_comment')
    user = models.ForeignKey(AmateurUser,
                             on_delete=models.CASCADE,
                             related_name='user_comment')
    name = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class SendingMessage(models.Model):
    user = models.ForeignKey(AmateurUser,
                             related_name='sending_messages',
                             on_delete=models.CASCADE)
    receive_user = models.ForeignKey(AmateurUser,
                                     related_name='receive_user',
                                     on_delete=models.PROTECT)
    subject = models.CharField(verbose_name='件名',
                               max_length=150)
    text = models.TextField(verbose_name='本文')
    sending_date = models.DateTimeField(auto_now_add=True)
    receiving_date = models.DateTimeField(auto_now_add=True)


class ReceiveMessage(models.Model):
    user = models.ForeignKey(AmateurUser,
                             related_name='receive_messages',
                             on_delete=models.CASCADE)
    sending_user = models.ForeignKey(AmateurUser,
                                     related_name='sending_user',
                                     on_delete=models.PROTECT)
    subject = models.CharField(verbose_name='件名',
                               max_length=150)
    text = models.TextField(verbose_name='本文')
    sending_date = models.DateTimeField(auto_now_add=True)
    receiving_date = models.DateTimeField(auto_now_add=True)
