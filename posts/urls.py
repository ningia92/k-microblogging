from django.urls import path

from posts import views

urlpatterns = [
    path("feed/explore", views.ExploreFeedView.as_view()),
    path("me/feed", views.HomeFeedView.as_view()),
]
