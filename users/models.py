from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    pass


class Follow(models.Model):
    # No index on follower: the implicit unique constraint's index on
    # (follower_id, followee_id) already covers lookups by follower_id
    follower = models.ForeignKey(
        User, related_name="followees", on_delete=models.CASCADE, db_index=False
    )
    followee = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=~Q(follower=F("followee")),
                name="follower_not_equal_followee",
            ),
            models.UniqueConstraint(
                fields=["follower", "followee"], name="unique_follow"
            ),
        ]
