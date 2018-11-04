from rest_framework import serializers

from articles.models import ArticleModel, RevisionModel


class RevisionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = RevisionModel
        fields = ('id', 'title', 'text')

    def create(self, validated_data):
        title = validated_data.get('title')
        article = ArticleModel.objects.filter(title=title).first()

        rev = RevisionModel.objects.create(
            article=article,
            text=validated_data['text'],
        )

        return rev


class ArticleSerializer(serializers.ModelSerializer):
    text = serializers.CharField(write_only=True)

    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'text')

    def create(self, validated_data):
        article = ArticleModel.objects.create(
            title=validated_data['title'],
            user=validated_data.get('user'),
        )

        RevisionModel.objects.create(
            article=article,
            text=validated_data['text'],
        )

        # FIXME: commit in one transaction
        return article
