from django.contrib.auth import get_user_model
from rest_framework import serializers
from articles.models import ArticleModel, RevisionModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('-created_at')[:1]
        return super(FilteredListSerializer, self).to_representation(data)


class RevisionLastSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = RevisionModel
        fields = ('id', 'title', 'text')
        list_serializer_class = FilteredListSerializer

    def create(self, validated_data):
        title = validated_data.get('title')
        article = ArticleModel.objects.filter(title=title).first()

        RevisionModel.objects.create(
            article=article,
            text=validated_data['text'],
        )

        return article


class RevisionListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RevisionModel
        fields = ('id', 'text', 'user', 'ip_addr', 'created_at')


class ArticleSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True)
    revision = RevisionLastSerializer(read_only=True, many=True)

    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'text', 'revision')

    def create(self, validated_data):
        article = ArticleModel.objects.create(title=validated_data['title'])

        RevisionModel.objects.create(
            user=validated_data.get('user'),
            article=article,
            text=validated_data['text'],
            ip_addr=validated_data['ip_addr'],
        )

        # FIXME: save single commit !!!
        return article

    def update(self, article, validated_data):
        print('upd')
        RevisionModel.objects.create(
            article=article,
            text=validated_data['text'],
        )
        return article
