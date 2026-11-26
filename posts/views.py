from django.db.models import Q
from rest_framework import generics

from posts.models import Post
from posts.serializers import PostSerializer
from users.models import Follow


class ExploreFeedView(generics.ListAPIView):
    queryset = (
        Post.objects.select_related("author")
        .prefetch_related("topics")
        .order_by("-created_at")[:20]
    )
    serializer_class = PostSerializer


class HomeFeedView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        followees = Follow.objects.filter(follower=self.request.user).values("followee")

        return (
            Post.objects.select_related("author")
            .prefetch_related("topics")
            .filter(Q(author__in=followees) | Q(author=self.request.user))
            .order_by("-created_at")[:20]
        )
