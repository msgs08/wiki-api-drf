from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import ArticleModel, RevisionModel
from articles.serializers import ArticleSerializer, RevisionLastSerializer, RevisionListSerializer

User = get_user_model()


class ArticleReadView(generics.RetrieveAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer


class ArticlesListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = ArticleModel.objects.order_by('-created_at').all()


class RevisionsView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, article_id):
        revs = RevisionModel.objects.filter(article_id=article_id).order_by('-created_at').all()
        serializer = RevisionListSerializer(revs, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleAddView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    get_serializer = ArticleSerializer

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_addr=ip)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ArticleEditView(UpdateAPIView):
    permission_classes = (AllowAny,)
    get_serializer = ArticleSerializer
    queryset = ArticleModel.objects

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

