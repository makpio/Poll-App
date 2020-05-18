from django.test import TestCase

# Create your tests here.
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse


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

def createQuestion(questionText, days):
    
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(questionText=questionText, pubDate=time)


class QuestionIndexViewTests(TestCase):
    def testNoQuestions(self):
    
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latestQuestionList'], [])

    def testPastQuestion(self):
       
        # Questions with a pub_date in the past are displayed on the
        # index page.
        
        createQuestion(questionText="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latestQuestionList'],
            ['<Question: Past question.>']
        )

    def testFutureQuestion(self):
        
        # Questions with a pub_date in the future aren't displayed on
        # the index page.
        
        createQuestion(questionText="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latestQuestionList'], [])

    def testFutureQuestionAndPastQuestion(self):
        
        # Even if both past and future questions exist, only past questions
        # are displayed.
        
        createQuestion(questionText="Past question.", days=-30)
        createQuestion(questionText="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latestQuestionList'],
            ['<Question: Past question.>']
        )

    def testTwoPastQuestions(self):
       
        # The questions index page may display multiple questions.
       
        createQuestion(questionText="Past question 1.", days=-30)
        createQuestion(questionText="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latestQuestionList'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )