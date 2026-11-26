from rest_framework import serializers

from posts.models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    topics = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Post
        fields = ["id", "author", "text", "topics", "created_at"]
