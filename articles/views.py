from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import ArticleModel, RevisionModel
from articles.serializers import ArticleSerializer, RevisionSerializer


# class ArticleReadView(RetrieveAPIView):
#     serializer_class = ArticleSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     lookup_field = "title"
#
#     def get_queryset(self):
#         articles = ArticleModel.objects.all()
#         print('get queryset ::', )
#         return articles


class ArticleReadView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # serializer_class = ArticleSerializer

    def get(self, request, title):
        print('get:')
        article = ArticleModel.objects.filter(title=title).first()
        last_rev = RevisionModel.objects.filter(article_id=article.id).order_by('-created_at').first()

        data = {
            'id': article.id,
            'title': article.title,
            'counter': article.counter,
            'text': last_rev.text,
        }

        return Response(data, status=status.HTTP_201_CREATED)


class ArticlesListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = ArticleModel.objects.all()


class RevisionsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, title):
        print('get:')
        article = ArticleModel.objects.filter(title=title).first()
        revs = RevisionModel.objects.filter(article_id=article.id).order_by('-created_at').all()

        serializer = RevisionSerializer(revs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleAddView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer
    get_serializer = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleEditView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    get_serializer = RevisionSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
