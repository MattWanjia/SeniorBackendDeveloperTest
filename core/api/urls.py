from django.urls import path, include
from rest_framework import routers
from .views import Last25StoriesApiView, LastWeekWords, UserKarmaStoryCount


urlpatterns = [
    path('last25new', Last25StoriesApiView.as_view()),
    path('lastweek', LastWeekWords.as_view()),
    path('user600story', UserKarmaStoryCount.as_view())
]