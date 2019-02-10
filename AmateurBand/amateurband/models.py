from django.contrib.auth import get_user_model
from django.db import models
from stdimage.models import StdImageField
AmateurUser = get_user_model()

AGE_CHOICES = (
        (1, '10～20歳'),
        (2, '20～30歳'),
        (3, '30～40歳'),
        (4, '40～50歳'),
        (5, '50～60歳'),
        (6, '60～70歳'),
    )
GENDER_CHOICES = (
    (1, '男性'),
    (2, '女性'),
)
RECRUITMENT_GENDER_CHOICES = (
    (1, '男性'),
    (2, '女性'),
    (3, '男女問わない')
)
INSTRUMENT_CHOICES = (
        ('ヴォーカル', 'ヴォーカル'),
        ('ギター', 'ギター'),
        ('ベース', 'ベース'),
        ('ドラム', 'ドラム'),
        ('キーボード', 'キーボード'),
        ('その他', 'その他'),
    )
LEVEL_CHOICES = (
    ('初心者', '初心者'),
    ('経験者', '経験者'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(AmateurUser,
                                related_name='profile',
                                on_delete=models.CASCADE)
    image = StdImageField(upload_to='amateur_image/', blank=True, null=True, variations={
        'large': (600, 400),
        'thumbnail': (120, 120, True),
        'medium': (300, 200),
    })
    gender = models.IntegerField(verbose_name='性別',
                                 choices=GENDER_CHOICES,
                                 null=True,
                                 blank=True)
    age = models.IntegerField(verbose_name='年齢',
                              choices=AGE_CHOICES,
                              blank=True, null=True)
    instrument = models.CharField(max_length=10,
                                  verbose_name='パート楽器',
                                  choices=INSTRUMENT_CHOICES,
                                  blank=True, null=True)
    amateur_level = models.CharField(max_length=10,
                                     verbose_name='初心者？経験者？',
                                     choices=LEVEL_CHOICES,
                                     blank=True, null=True)
    area = models.CharField(verbose_name='活動地域',
                            max_length=100,
                            blank=True, null=True)


class SearchWord(models.Model):
    user = models.ForeignKey(AmateurUser,
                             related_name='searchwords',
                             on_delete=models.CASCADE)
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word


class Footprint(models.Model):
    user = models.OneToOneField(AmateurUser, on_delete=models.CASCADE)
    footprint_user = models.ManyToManyField(AmateurUser,
                                            blank=True,
                                            related_name='footprints_user')


class Recruitment(models.Model):

    public = models.BooleanField(default=False, verbose_name='公開しない')
    user = models.ForeignKey(AmateurUser,
                             related_name='recruitment',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='タイトル')
    gender = models.IntegerField(verbose_name='性別対象',
                                 choices=RECRUITMENT_GENDER_CHOICES)
    instrument = models.CharField(max_length=10,
                                  verbose_name='募集楽器',
                                  choices=INSTRUMENT_CHOICES,)
    amateur_level = models.BooleanField(default=False, verbose_name='初心者歓迎')
    age = models.IntegerField(verbose_name='年齢制限',
                              choices=AGE_CHOICES,)
    area = models.CharField(verbose_name='活動地域', max_length=100)
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
    admission = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class SendingMessage(models.Model):
    sending_user = models.ForeignKey(AmateurUser,
                                     related_name='sending_messages',
                                     on_delete=models.CASCADE)
    receive_user = models.ForeignKey(AmateurUser,
                                     related_name='to_user',
                                     on_delete=models.CASCADE)
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
                                     related_name='message_route_user',
                                     on_delete=models.CASCADE)
    subject = models.CharField(verbose_name='件名',
                               max_length=150)
    text = models.TextField(verbose_name='本文')
    unread = models.BooleanField(default=False)
    sending_date = models.DateTimeField(auto_now_add=True)
    receiving_date = models.DateTimeField(auto_now_add=True)
