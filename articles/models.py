from django.conf import settings
from django.db import models


class ArticleModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=120, unique=True)
    counter = models.BigIntegerField(default=0)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'


class RevisionModel(models.Model):
    article = models.ForeignKey(ArticleModel, related_name='revision', on_delete=models.CASCADE)
    parent_id = models.IntegerField(default=0)
    comment = models.TextField(max_length=120)
    text = models.TextField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'revisions'
        ordering = ('created_at',)
