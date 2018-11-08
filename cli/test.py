import os
import sys
import django

# run Django standalone script
from django.contrib.auth import get_user_model
from django.db import transaction

sys.path.append("/home/akpp/projects/sensumfms_back")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki.settings")
django.setup()

from articles.serializers import ArticleSerializer
from articles.models import ArticleModel, RevisionModel

User = get_user_model()

if __name__ == '__main__':
    import logging

    l = logging.getLogger('django.db.backends')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiki.settings')

    # r = RevisionModel.objects.all()
    # a = ArticleModel.objects.filter(revisions__text__contains='cont')

    a = ArticleModel.objects.filter(title='aaa19').first()
    # print('query:', a.query, a.all())
    # print('model', a.all())
    # r = RevisionModel.objects.filter(article_id=a.id).order_by('-created_at').first()
    # print('r', r)
    # s = ArticleSerializer(a)
    # print('data:', s.data)
    # print(s.is_valid())
    # print('artd:', art.validated_data)

    arts = ArticleModel.objects.all()
    print('arts', arts.query)
