from django.conf import settings
from django.db import models
from django.db.models import Q


class Post(models.Model):
    text = models.CharField(max_length=500)
    # No index on author: the index on (author_id, created_at)
    # already covers lookup by author_id
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
        db_index=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"], name="posts_order_idx"),
            models.Index(
                fields=["author", "created_at"], name="author_posts_order_idx"
            ),
        ]


class Topic(models.TextChoices):
    MATHEMATICS = "mathematics", "Mathematics"
    PHYSICS = "physics", "Physics"
    CHEMISTRY = "chemistry", "Chemistry"
    BIOLOGY = "biology", "Biology"
    MEDICINE = "medicine", "Medicine"
    NEUROSCIENCE = "neuroscience", "Neuroscience"
    ASTRONOMY = "astronomy", "Astronomy"
    EARTH_SCIENCES = "earth_sciences", "Earth Sciences"
    COMPUTER_SCIENCE = "computer_science", "Computer Science"
    ENGINEERING = "engineering", "Engineering"
    PSYCHOLOGY = "psychology", "Psychology"
    SOCIAL_SCIENCES = "social_sciences", "Social Sciences"
    PHILOSOPHY_OF_SCIENCE = "philosophy_of_science", "Philosophy of Science"


class PostTopic(models.Model):
    name = models.CharField(max_length=30, choices=Topic)
    # No index on post: the implicit unique constraint's index on
    # (post_id, name) is enough to retrieve the topics of a post
    post = models.ForeignKey(
        Post, related_name="topics", on_delete=models.CASCADE, db_index=False
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(name__in=Topic.values), name="topic_in_topics_group"
            ),
            models.UniqueConstraint(
                fields=["post", "name"], name="unique_post_topic_pair"
            ),
        ]
