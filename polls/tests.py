from django.test import TestCase

# Create your tests here.
import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def testWasPublishedRecentlyWithFutureQuestion(self):
        
        # was_published_recently() returns False for questions whose pubDate
        # is in the future.
        
        time = timezone.now() + datetime.timedelta(days = 1)
        futureQuestion = Question(pubDate = time)
        self.assertIs(futureQuestion.wasPublishedRecently(), False)

    def testWasPublishedRecentlyWithOldQuestion(self):
    
        # wasPublishedRecently() returns False for questions whose pubDate
        # is older than 1 day.
    
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        oldQuestion = Question(pubDate=time)
        self.assertIs(oldQuestion.wasPublishedRecently(), False)

    def testWasPublishedRecentlyWithRecentQuestion(self):
  
        # wasPublishedRecently() returns True for questions whose pubDate
        # is within the last day.

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recentQuestion = Question(pubDate=time)
        self.assertIs(recentQuestion.wasPublishedRecently(), True)