from django.test import TestCase, Client
from unittest.mock import patch

from .models import Article, Source
from .views import newsfeed
from .news_scraper import retrieve_news, store_news, update_news

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

# Testing the logic of the functionality related to news features, article aggregation, user subscriptions, reactions, and comments

# tests for news/news_scraper.py implementation
class TestNewsScraper(TestCase):

    # mock requests.get method 
    @patch('news.news_scraper.requests.get')
    def test_retrieve_news(self, mock_get):
        mock_data = {
            'articles': [
                {   
                    'title': 'Mock request',
                    'description': 'Mock request desc',
                    'url': 'https://mock-article.com/',
                    'publishedAt': '2023-06-15T00:00:00Z',
                    'source': {
                        'id': 'mock-source-id',
                        'name': 'Mock Source',
                    },
                    'urlToImage': '', # test accept null thumbnail
                },
            ]
        }

        mock_response = type('MockReponse', (object,), {'status_code': 200, 'json': lambda self: mock_data})()

        mock_get.return_value = mock_response

        news_data = retrieve_news('mock-country')

        self.assertEqual(news_data, mock_data)


    # mock retrieve_news method from news/news_scraper.py
    @patch('news.news_scraper.retrieve_news')
    def test_store_news(self, mock_retrieve_news):
        mock_data = {
           'articles': [
                {
                    'title': 'Test article',
                    'description': 'This is a test article',
                    'url': 'https://example.com/test-article',
                    'publishedAt': '2023-04-25T00:00:00Z',
                    'source': {
                        'id': 'test-source',
                        'name': 'Test Source'
                    },
                    'urlToImage': 'https://example.com/test-thumbnail.jpg',
                },
                {
                    'title': 'Test article 2',
                    'description': 'This is another test article',
                    'url': 'https://example.com/test-article-2',
                    'publishedAt': '2023-06-15T00:00:00Z',
                    'source': {
                        'id': 'test-source-2',
                        'name': 'Test Source 2'
                    },
                    'urlToImage': 'https://example.com/test-thumbnail2.jpg',
                }
            ]
        }

        mock_retrieve_news.return_value = mock_data

        store_news(mock_data)

        article = Article.objects.get(title='Test article')
        self.assertEqual(article.description, 'This is a test article')
        self.assertEqual(article.source.name, 'Test Source')
        self.assertEqual(article.thumbnail_url, 'https://example.com/test-thumbnail.jpg')

        article2 = Article.objects.get(title='Test article 2')
        self.assertEqual(article2.description, 'This is another test article')
        self.assertEqual(article2.source.name, 'Test Source 2')
        self.assertEqual(article2.thumbnail_url, 'https://example.com/test-thumbnail2.jpg')
    

    @patch('news.news_scraper.retrieve_news')
    @patch('news.news_scraper.store_news')
    def test_update_news(self, mock_store_news, mock_retrieve_news):
            mock_news_data = {
                 'articles': [
                    {
                        'title': 'Test article',
                        'description': 'This is a test article',
                        'url': 'https://example.com/test-article',
                        'publishedAt': '2023-04-25T00:00:00Z',
                        'source': {
                            'id': 'test-source',
                            'name': 'Test Source'
                        },
                        'urlToImage': 'https://example.com/test-thumbnail.jpg',
                    },
                    {
                        'title': 'Test article 2',
                        'description': 'This is another test article',
                        'url': 'https://example.com/test-article-2',
                        'publishedAt': '2023-06-15T00:00:00Z',
                        'source': {
                            'id': 'test-source-2',
                            'name': 'Test Source 2'
                        },
                        'urlToImage': 'https://example.com/test-thumbnail2.jpg',
                    }
                 ]
            }

            mock_retrieve_news.side_effect = [mock_news_data, mock_news_data, mock_news_data]

            update_news()

            i = 0
            while i < 3:
                mock_retrieve_news.assert_called
                mock_store_news.assert_called_with(mock_news_data)
                i = i + 1


# Tests include the views which handle the delivery of news to users.
class TestNewsViews(TestCase):
    def setUp(self):
         self.client = Client()

         self.user = User.objects.create_user(
              username='newstestuser',
              password='pressPASS100'
         )

         self.source1 = Source.objects.create(name='Source 1')
         self.source2 = Source.objects.create(name='Source 2')

         self.article1 = Article.objects.create(
              title='Test article 1',
              description='This is a test article',
              url='https://example.com/article-2',
              published_at='2023-04-25T00:00:00Z',
              source=self.source1,
              thumbnail_url=''
         )

         self.article2 = Article.objects.create(
              title='Test article 2',
              description='This is a test article',
              url='https://example.com/article-2',
              published_at='2023-04-25T00:00:00Z',
              source=self.source1,
              thumbnail_url='https://example-com/article-2-thumbnail.jpg'
         )

         self.article3 = Article.objects.create(
              title='Test article 3',
              description='This is another test article',
              url='https://example.com/article-3',
              published_at='2023-04-25T00:00:00Z',
              source=self.source2,
              thumbnail_url='https://example.com/article-3-thumbnail.jpg'
         )

    def test_logged_in_user(self):
         self.client.login(username='newstestuser', password='pressPASS100')
         self.user.sources.add(self.source1)

         response = self.client.get(reverse('newsfeed'))
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'newsfeed.html')
         self.assertEqual(len(response.context['articles']), 2)
         self.assertContains(response, 'Test article 1')
         self.assertContains(response, 'Test article 2')