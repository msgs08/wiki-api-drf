from rest_framework import serializers

from articles.serializers import UserSerializer
from .models import NoteModel


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = NoteModel
        fields = ('id', 'user', 'content', 'created_at')

    def create(self, validated_data):
        post = NoteModel.objects.create(
            user=validated_data['user'],
            content=validated_data['content'],
        )

        return post
