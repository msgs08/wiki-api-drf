from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from articles.models import ArticleModel
from articles.serializers import ArticleSerializer
from articles.views import ArticleAddView, ArticleEditView


class ArticleTestCase(TestCase):
    def setUp(self):
        self.title = 'same title'
        self.text = 'same text'

    def test_create(self):
        factory = APIRequestFactory()
        request = factory.post('/articles/add/', {'title': self.title, 'text': self.text})

        view = ArticleAddView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ArticleModel.objects.count(), 1)

        article = ArticleModel.objects.filter(title=self.title).first()
        self.assertIsInstance(article, ArticleModel)
        serializer = ArticleSerializer(article)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data['revision']), 1)
        self.assertEqual(response.data['title'], self.title)
        self.assertEqual(response.data['revision'][0]['text'], self.text)

    def test_update(self):
        self.test_create()
        article = ArticleModel.objects.filter(title=self.title).first()
        self.assertIsInstance(article, ArticleModel)

        factory = APIRequestFactory()
        data = {'title': self.title, 'text': '{} edited'.format(self.text)}
        request = factory.put('/articles/edit/', data)

        view = ArticleEditView.as_view()
        response = view(request, pk=article.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(ArticleModel.objects.count(), 1)
