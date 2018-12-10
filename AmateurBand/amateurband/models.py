from django.conf import settings
from django.db import models

AmateurUser = settings.AUTH_USER_MODEL


class Article(models.Model):
    class Meta:
        db_table = 'article'

    user = models.ForeignKey(AmateurUser,
                             verbose_name='ユーザー',
                             on_delete=models.CASCADE,
                             related_name='articles')
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title
