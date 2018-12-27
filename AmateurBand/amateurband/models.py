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


class Profile(models.Model):
    GENDER_CHOICES = (
        ('男性', '男性'),
        ('女性', '女性'),
    )

    class Meta:
        db_table = 'profile'

    user = models.OneToOneField(AmateurUser,
                                on_delete=models.CASCADE,
                                related_name='profile')
    nickname = models.CharField(max_length=100, verbose_name='ニックネーム')

    gender = models.CharField(max_length=2, verbose_name='性別',
                              choices=GENDER_CHOICES)
    age = models.IntegerField(verbose_name='年齢制限',
                              choices=AGE_CHOICES)
    instrument = models.CharField(max_length=100, verbose_name='担当楽器',
                                  choices=INSTRUMENT_CHOICES)


class Article(models.Model):
    class Meta:
        db_table = 'article'

    user = models.ForeignKey(AmateurUser,
                             related_name='articles',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Recruitment(models.Model):

    user = models.ForeignKey(AmateurUser,
                             related_name='recruitment',
                             on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True, verbose_name='記事を公開する')
    title = models.CharField(max_length=100, verbose_name='タイトル')
    instrument = models.CharField(max_length=10,
                                  verbose_name='募集楽器',
                                  choices=INSTRUMENT_CHOICES,
                                  blank=True, null=True)
    amateur_level = models.BooleanField(default=False, verbose_name='初心者歓迎')
    age = models.IntegerField(verbose_name='年齢制限',
                              choices=AGE_CHOICES,
                              blank=True, null=True)
    comment = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
