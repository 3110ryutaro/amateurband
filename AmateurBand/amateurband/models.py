from django.contrib.auth import get_user_model
from django.db import models

AmateurUser = get_user_model()


class Article(models.Model):
    class Meta:
        db_table = 'article'

    user = models.ForeignKey(AmateurUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
