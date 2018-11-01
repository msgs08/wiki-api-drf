import os
import sys
import django

# run Django standalone script

sys.path.append("/home/akpp/projects/sensumfms_back")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki.settings")
django.setup()

from articles.serializers import ArticleSerializer
from articles.models import ArticleModel, RevisionModel

if __name__ == '__main__':
    import logging

    l = logging.getLogger('django.db.backends')
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wiki.settings')

    a = ArticleModel.objects.filter(title='aaa19').first()
    print('model', a)

    r = RevisionModel.objects.filter(article_id=a.id).order_by('-created_at').first()
    print('r', r)

    # s = ArticleSerializer(m)
    # print(art.is_valid())
    # print('artd:', s.data)
    # print('artd:', art.validated_data)
