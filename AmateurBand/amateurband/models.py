from django.contrib.auth import get_user_model
from django.db import models

AmateurUser = get_user_model()


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
    AGE_CHOICES = (
        (1, '10～20'),
        (2, '20～30'),
        (3, '30～40'),
        (4, '40～50'),
        (5, '50～60'),
        (6, '60～70'),
    )
    INSTRUMENT_CHOICES = (
        ('ヴォーカル', 'ヴォーカル'),
        ('ギター', 'ギター'),
        ('ベース', 'ベース'),
        ('ドラム', 'ドラム'),
        ('キーボード', 'キーボード'),
        ('その他', 'その他'),
    )
    user = models.ForeignKey(AmateurUser,
                             related_name='recruitment',
                             on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    instrument = models.CharField(max_length=10,
                                  verbose_name='募集楽器',
                                  choices=INSTRUMENT_CHOICES,
                                  blank=True, null=True)
    amateur_level = models.BooleanField(default=False)
    age = models.IntegerField(verbose_name='年齢',
                              choices=AGE_CHOICES,
                              blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
