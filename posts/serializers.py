from rest_framework import serializers

from articles.serializers import UserSerializer
from posts.models import PostModel


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostModel
        fields = ('id', 'user', 'content')

    def create(self, validated_data):
        post = PostModel.objects.create(
            user=validated_data['user'],
            content=validated_data['content'],
        )

        return post
